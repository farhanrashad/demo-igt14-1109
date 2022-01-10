# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class transferTaskStage(models.Model):
    _name = 'stock.transfer.order.stage.line'
    _description = 'Order Stages'
    _order = 'sequence'
    
    stock_order_transfer_id = fields.Many2one('stock.transfer.order', string='Transfer Order', index=True, required=True, ondelete='cascade')
    
    stage_id = fields.Many2one('stock.transfer.order.stage', string='Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    sequence = fields.Integer(string='Sequence')
    next_stage_id = fields.Many2one('stock.transfer.order.stage', string='Next Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    prv_stage_id = fields.Many2one('stock.transfer.order.stage', string='Previous Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    
    transfer_exception_type_id = fields.Many2one("stock.transfer.exception.type", string="Exception Type", )
    
            
class StockTransferOrder(models.Model):
    _name = 'stock.transfer.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Stock Transfer Order'
    _order = 'date_order desc, id desc'
    _check_company_auto = True

    def _get_default_stage_id(self):
        return self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('stage_category','=','draft')], order='sequence', limit=1)
    
    def _get_type_id(self):
        return self.env['stock.transfer.order.type'].search([], limit=1)
    
    def _get_default_category_id(self):
        return self.env['stock.transfer.order.category'].search([('transfer_order_type_id','=',self.transfer_order_type_id.id)], limit=1)
    
    
    def _get_default_location(self):
        location_id = self.env['stock.location'].search([('return_location','=',True)],limit=1)
        return location_id
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string='Transfer Type', index=True, required=True, default=_get_type_id, readonly=True, copy=False, )
    code = fields.Char(related='transfer_order_type_id.code')
    sequence_code = fields.Char(string="Sequence Code")
    
    transfer_order_category_id = fields.Many2one('stock.transfer.order.category', string='Transfer Category', index=True, readonly=True, copy=False, domain="[('transfer_order_type_id','=',transfer_order_type_id)]",default=_get_default_category_id)
    order_stage_ids = fields.One2many('stock.transfer.order.stage.line', 'stock_order_transfer_id', string='Stage', copy=True)
        
    action_type = fields.Selection(related='transfer_order_category_id.action_type')
    disallow_staging = fields.Boolean(related='transfer_order_type_id.disallow_staging')
    filter_products = fields.Boolean(related='transfer_order_category_id.filter_products')
    categ_control_ids = fields.Many2many(related='transfer_order_category_id.categ_control_ids')
    
    partner_id = fields.Many2one('res.partner', 'Contractor',check_company=True, readonly=True, )
    
    stage_id = fields.Many2one('stock.transfer.order.stage', string='Stage', compute='_compute_stage_id', store=True, readonly=False, ondelete='restrict', tracking=True, index=True, default=_get_default_stage_id, copy=False, )
    #stage_id = fields.Many2one('stock.transfer.order.stage', string='Stage', store=True, readonly=False, ondelete='restrict', tracking=True, index=True, copy=False, default=_get_default_stage_id)
    picking_state = fields.Char(string='Picking State', compute='_compute_picking_state',
        store=True, copy=False, readonly=True,)
    
    next_stage_id = fields.Many2one('stock.transfer.order.stage', string='Next Stage', compute='_compute_order_stage')
    prv_stage_id = fields.Many2one('stock.transfer.order.stage', string='Previous Stage', compute='_compute_order_stage')
    last_stage_id = fields.Many2one('stock.transfer.order.stage',string='Last Stage')
    stage_category = fields.Selection(related='stage_id.stage_category')
    allow_transactions = fields.Boolean(related='stage_id.allow_transactions')
    next_stage_category = fields.Selection(related='next_stage_id.stage_category', string='Next Stage Category')
    prv_stage_category = fields.Selection(related='next_stage_id.stage_category', string='Previous Stage Category')
    stage_code = fields.Char(related='stage_id.stage_code')
    
    #exceptions or transactions
    transfer_exception_type_ids = fields.Many2many("stock.transfer.exception.type", string="Exception Type")
    #transaction_code = fields.Char(related='transfer_exception_type_id.code', string='T Code')
    #txn_stage_id = fields.Many2one('stock.transfer.order.stage', related='transfer_exception_type_id.stage_id', string='TXN Stage')
    
    #exception with multiple lines
    stock_transfer_txn_line = fields.One2many('stock.transfer.txn.line', 'stock_transfer_order_id', string='Transaction Line', copy=False, auto_join=True,)
    #transfer_txn_type_ids = fields.Many2many("stock.transfer.exception.type", string="TXN Types", domain="[('transfer_order_type_id','=',transfer_order_type_id)]")
    curr_txn_type_id = fields.Many2one("stock.transfer.exception.type", string="Currenct TXN Type", compute='_compute_all_txn')
    txn_stage_ids = fields.Many2many("stock.transfer.order.stage", string="TXN Stages", compute='_compute_all_txn')
    curr_txn_stage_id = fields.Many2one("stock.transfer.order.stage", related='curr_txn_type_id.stage_id')
    message_type = fields.Selection(related='curr_txn_type_id.message_type')
    exception_message = fields.Char(related='curr_txn_type_id.message', string='Exception')

    #closing reasons
    disable_close = fields.Boolean(string='Close Disable')
    close_reason_id = fields.Many2one("stock.transfer.close.reason", string="Close Reason", copy=False, tracking=True, readonly=True)
    close_reason_message = fields.Char(string='Close Message', copy=False, readonly=True)
    date_closed = fields.Datetime(string='Closed Date', copy=False, readonly=True)

    date_request = fields.Datetime(string='Request Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Order request date")
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Order confirmation date")
    date_scheduled = fields.Datetime(string='Date Scheduled', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Deadline schedule date")
    delivery_deadline = fields.Datetime(string='Delivery Deadline', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Delivery Deadline")
    order_deadline = fields.Datetime(string='Order Exipiry', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Order Expiry")

    
    return_deadline = fields.Datetime(string='Return Deadline', readonly=False, compute='_compute_return_deadline', store=True, copy=False, help="Retrun Material Deadline")
    date_delivered = fields.Datetime(string="Actual Delivery", compute="_compute_all_dates", store=True)
    date_returned = fields.Datetime(string="Actual Return", compute="_compute_all_dates", store=True)
    
    stock_transfer_order_line = fields.One2many('stock.transfer.order.line', 'stock_transfer_order_id', string='Transfer Line', copy=True, auto_join=True,readonly=True, )
    
    stock_transfer_return_line = fields.One2many('stock.transfer.return.line', 'stock_transfer_order_id', string='Return Transfer Line', copy=True, auto_join=True, )

        
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, readonly=True, )
    description = fields.Text()
    user_id = fields.Many2one('res.users', string="Request Owner",check_company=True, domain="[('company_ids', 'in', company_id)]", default=lambda self: self.env.user, required=True,readonly=True)
    
    delivery_count = fields.Integer(compute='_compute_picking_count', string='Number of Delivery')
    return_count = fields.Integer(compute='_compute_picking_count', string='Number of Return')
    picking_ids = fields.One2many('stock.picking', 'stock_transfer_order_id', string='Picking')
    bill_count = fields.Integer(compute='_compute_bill_count')

    location_src_id = fields.Many2one('stock.location', string='Source Location',  )
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', )
    picking_type_id = fields.Many2one('stock.picking.type',  )
    picking_type_code = fields.Selection(related='picking_type_id.code')
    return_location_id = fields.Many2one('stock.location', string='Return Location',  )
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence', copy=False, check_company=True)
    
    #document fields
    health_check_form = fields.Boolean(related='transfer_order_category_id.health_check_form')
    fir_report = fields.Boolean(related='transfer_order_category_id.fir_report')
    accident_report = fields.Boolean(related='transfer_order_category_id.accident_report')
    hoto_checklist = fields.Boolean(related='transfer_order_category_id.hoto_checklist')
    proof_attachment = fields.Boolean(related='transfer_order_category_id.proof_attachment')
    
    file_health_check = fields.Binary(string='Health Check Form')
    file_fir = fields.Binary(string='FIR Report')
    file_accident_report = fields.Binary(string='Accident Report')
    file_hoto_checklist = fields.Binary(string='HOTO Checklist Form')
    file_proof_attachment = fields.Binary(string='Proof Attachment')
    
    
    #optional fields
    #has_penalty = fields.Boolean(related="transfer_order_category_id.has_penalty", ondelete='set default')
    #has_closed = fields.Boolean(related="transfer_order_category_id.has_closed", ondelete='set default')
    
    has_partner = fields.Selection(related="transfer_order_category_id.has_partner")
    has_reference = fields.Selection(related="transfer_order_category_id.has_reference")
    has_purchase_order = fields.Selection(related="transfer_order_category_id.has_purchase_order")
    has_transfer_order = fields.Selection(related="transfer_order_category_id.has_transfer_order")
    has_transporter = fields.Selection(related="transfer_order_category_id.has_transporter")
    has_analytic_account = fields.Selection(related="transfer_order_category_id.has_analytic_account")
    has_analytic_tags = fields.Selection(related="transfer_order_category_id.has_analytic_tags")
    has_supplier = fields.Selection(related="transfer_order_category_id.has_supplier")
    has_tower_info = fields.Selection(related="transfer_order_category_id.has_tower_info")

    
    reference = fields.Char(string="Reference")
    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Transfer Order')
    transporter_id = fields.Many2one('res.partner', string='Transporter')
    
    partner_category_ids = fields.Many2many('res.partner.category', related='transfer_order_category_id.partner_category_ids')
    transporter_category_ids = fields.Many2many('res.partner.category', related='transfer_order_category_id.transporter_category_ids')

    allow_special_edit = fields.Boolean(related='stage_id.allow_special_edit')
    special_edit_mode = fields.Boolean(string='Special Edit Mode')
    @api.depends('transfer_order_category_id','stock_transfer_txn_line')
    def _compute_all_picking(self):
        for order in self:
            picking_type_id = return_picking_type_id = False
            location_src_id = False
            location_dest_id = False
            return_location_id = False
            
            for txn in order.stock_transfer_txn_line:
                if txn.transfer_exception_type_id.picking_type_id:
                    picking_type_id = txn.transfer_exception_type_id.picking_type_id.id
                if txn.transfer_exception_type_id.location_src_id:
                    location_src_id = txn.transfer_exception_type_id.location_src_id.id
                if txn.transfer_exception_type_id.location_dest_id:
                    location_dest_id = txn.transfer_exception_type_id.location_dest_id.id
                #return
                if txn.transfer_exception_type_id.return_picking_type_id:
                    return_picking_type_id = txn.transfer_exception_type_id.return_picking_type_id.id
                if txn.transfer_exception_type_id.return_location_id:
                    return_location_id = txn.transfer_exception_type_id.return_location_id.id
            
            if not picking_type_id:
                picking_type_id = order.transfer_order_category_id.picking_type_id.id
            if not location_src_id:
                location_src_id = order.transfer_order_category_id.location_src_id.id
            if not location_dest_id:
                location_dest_id = order.transfer_order_category_id.location_dest_id.id
            if not return_picking_type_id:
                return_picking_type_id = order.transfer_order_category_id.return_picking_type_id.id
            if not return_location_id:
                if order.transfer_order_category_id.return_location_id:
                    return_location_id = order.transfer_order_category_id.return_location_id.id
                else:
                    return_location_id = order.transfer_order_category_id.return_picking_type_id.default_location_dest_id.id
                    
            order.picking_type_id = picking_type_id
            order.location_src_id = location_src_id
            order.location_dest_id = location_dest_id
            order.return_location_id = return_location_id
            
            for line in order.stock_transfer_order_line:
                if not line.location_dest_id:
                    line.location_dest_id = order.location_dest_id.id
                line.location_src_id = order.location_src_id.id
            for rline in order.stock_transfer_return_line:
                line.location_dest_id = order.return_location_id.id
                if not line.location_src_id:
                    line.location_src_id = order.location_dest_id.id
    
    
    @api.onchange('transfer_order_type_id')
    def _onchange_transfer_type_id(self):
        self.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('stage_category','=','draft')], order='sequence',limit=1).id
        self.sequence_code = self.code
   
    #@api.onchange('transfer_order_category_id')
    def _onchange_transfer_order_category_id(self):
        lines_data = []
        txn_ids = self.env['stock.transfer.exception.type'].search([('transfer_order_type_id','=',self.transfer_order_type_id.id),('transfer_order_category_id','=',self.transfer_order_category_id.id),('stage_auto_apply','=',True)])
        
        #if self.stock_transfer_txn_line:
            #self.stock_transfer_txn_line.unlink()
        #else:
        for txn in txn_ids:
            lines_data.append([0,0,{
                'transfer_exception_type_id': txn.id,
            }])
                #self.env['stock.transfer.txn.line'].create({
                #    'stock_transfer_order_id': self.id,
                #    'transfer_exception_type_id': txn.id,
                #})
        self.write({
            'stock_transfer_txn_line':lines_data,
        })
    
    #@api.onchange('transfer_exception_type_ids')
    def _transfer_exception_type_onchange(self):
        for order in self:
            if order.stage_id.stage_category == 'draft':
                if order.stock_transfer_order_line:
                    order.stock_transfer_order_line.unlink()
                for txn in order.transfer_exception_type_ids:
                    vals = {
                        'transfer_exception_type_id': txn.id,
                        'txn_action': 'open',
                    }
            
            
    @api.model
    def create(self, vals):            
        vals['name'] = (
        vals.get('code') or
        self.env.context.get('default_code') or
        self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('stock.transfer.order') or
         'New'
        )
        sequence = self.env['ir.sequence'].search([('prefix','=', vals['sequence_code'])
        ], limit=1)
        vals['sequence_id'] = sequence.id
        vals['name'] = sequence.next_by_id()
        transfer_order = super(StockTransferOrder, self).create(vals)        
        return transfer_order


    def unlink(self):
        if any(order.stage_category not in ('draft', 'cancel') for order in self):
            raise UserError(_('You can only delete draft requisitions.'))
        # Draft requisitions could have some requisition lines.
        self.mapped('stock.transfer.order.line').unlink()
        self.mapped('stock.transfer.return.line').unlink()
        self.mapped('stock.transfer.txn.line').unlink()
        return super(StockTransferOrder, self).unlink()
    
    def write(self,vals):
        stage_id = self.env['stock.transfer.order.stage'].browse(vals.get('stage_id'))
        txn_ids = self.env['stock.transfer.exception.type'].search([('apply_stage_id','=',self.stage_id.id),('stage_auto_apply','=',True)])
        result = super(StockTransferOrder, self).write(vals)
        #if 'stage_id' in vals:
        #raise UserError(_("stage =  '%s'.", self.stage_id.stage_category))
        #if self.stage_id.stage_category == 'draft':
        if self.order_stage_ids:
            self.order_stage_ids.unlink()
        self._compute_order_stages()
        return result
    
    def _compute_order_stages(self):
        vals = {}
        stages_list = []
        next_stage = prv_stage = False
        for order in self:
            stage_ids = self.env['stock.transfer.order.stage'].search([('transfer_order_category_ids', '=', order.transfer_order_category_id.id),('transfer_order_type_ids','=',order.transfer_order_type_id.id)])
            for stage in stage_ids:
                vals = {
                    'stock_order_transfer_id': order.id,
                    'stage_id': stage.id,
                }
                stages_list.append({
                    'stock_order_transfer_id': order.id,
                    'stage_id': stage.id, 
                    'sequence': stage.sequence,
                })
            #order.order_stage_ids.create(lines_data)
            for txn in order.stock_transfer_txn_line:
                #if not self.env['stock.transfer.order.stage.line'].search([('stage_id','=',txn.transfer_exception_type_id.stage_id.id)]):
                stages_list.append({
                    'stock_order_transfer_id': order.id,
                    'stage_id': txn.transfer_exception_type_id.stage_id.id, 
                    'sequence': txn.transfer_exception_type_id.stage_id.sequence,
                    'transfer_exception_type_id': txn.transfer_exception_type_id.id,
                })
                if txn.transfer_exception_type_id.next_stage_id.id:
                    stages_list.append({
                        'stock_order_transfer_id': order.id,
                        'stage_id': txn.transfer_exception_type_id.next_stage_id.id, 
                        'sequence': txn.transfer_exception_type_id.next_stage_id.sequence,
                        'transfer_exception_type_id': txn.transfer_exception_type_id.id,
                    }) 
            
            order.order_stage_ids.sudo().create(stages_list)
            #order.order_stage_ids = lines_data
            #===================================
            #++++++++Assign Next Stage++++++++++++++
            stages = self.env['stock.transfer.order.stage.line'].search([('stock_order_transfer_id','=', order.id)], order="sequence desc")
            for stage in stages:
                stage.sudo().update({
                    'next_stage_id': next_stage,
                })
                #if stage.transfer_exception_type_id.next_stage_id.id:
                    #next_stage = stage.transfer_exception_type_id.next_stage_id.id
                #else:
                next_stage = stage.stage_id.id
            #++++++++++++++++++++++++++++++++++++++++
            #+++++++++++Assign Previous Stage++++++++++
            stages = self.env['stock.transfer.order.stage.line'].search([('stock_order_transfer_id','=', order.id)], order="sequence asc")
            for stage in stages:
                stage.sudo().update({
                    'prv_stage_id': prv_stage,
                })
                #if stage.transfer_exception_type_id.prv_stage_id.id:
                    #prv_stage = stage.transfer_exception_type_id.next_stage_id.id
                #else:
                prv_stage = stage.stage_id.id
            #for order in order.order_stage_ids.sorted(key=lambda r: r.sequence):
                
    
    
    def _compute_order_stage(self):
        for order in self:
            next_stage = prv_stage = False
            for stage in order.order_stage_ids.filtered(lambda t: t.stage_id.id == order.stage_id.id):
                    next_stage = stage.next_stage_id.id
                    prv_stage = stage.prv_stage_id.id
            order.next_stage_id = next_stage
            order.prv_stage_id = prv_stage
    
    #@api.depends('stage_id','txn_stage_id')
    @api.depends('stage_id','curr_txn_stage_id')
    def _compute_next_stage(self):
        next_stage = self.stage_id.id
        for order in self:
            if order.curr_txn_type_id.exec_stage_id.id == order.stage_id.id:
                next_stage = order.curr_txn_stage_id.id
            else:
                if not order.curr_txn_stage_id.id == order.stage_id.id:
                    if order.curr_txn_stage_id.next_stage_id.id == order.stage_id.next_stage_id.id:
                        next_stage = self.curr_txn_stage_id.id
                    else:
                       next_stage = self.stage_id.next_stage_id.id 
                else:
                    next_stage = self.stage_id.next_stage_id.id
            #if not order.curr_txn_stage_id.id == order.stage_id.id:
             #   if order.curr_txn_stage_id.next_stage_id.id == order.stage_id.next_stage_id.id:
              #      next_stage = self.curr_txn_stage_id.id
               # else:
                #    next_stage = self.stage_id.next_stage_id.id
            #else:
                #next_stage = self.stage_id.next_stage_id.id
            order.next_stage_id = next_stage
        #for order in self:
        #    if not order.txn_stage_id.id == order.stage_id.id:
        #        if order.txn_stage_id.next_stage_id.id == order.stage_id.next_stage_id.id:
        #            next_stage = self.txn_stage_id.id
        #        else:
        #            next_stage = self.stage_id.next_stage_id.id
        #    else:
        #        next_stage = self.stage_id.next_stage_id.id
        #    order.next_stage_id = next_stage
    
    @api.model
    def cron_delivery_order_expiry(self):        
        today = fields.Datetime.now()
        # set to pending deliveries if date is in less than today
        domain_pending = [('delivery_deadline', '<', today),('stage_category', 'not in', ['close','cancel'])]
        order_pending = self.search(domain_pending)
        order_pending.set_close('delivery')
        
        return dict(order=order_pending.ids)
    
    @api.model
    def cron_return_order_expiry(self):        
        today = fields.Datetime.now()
        # set to pending deliveries if date is in less than today
        domain_pending = [('return_deadline', '<', today),('stage_category', 'not in', ['close','cancel'])]
        order_pending = self.search(domain_pending)
        order_pending.set_close('return')
        
        return dict(order=order_pending.ids)
    
    def set_close(self, type):
        #today = fields.Date.from_string(fields.Date.context_today(self))
        today = fields.Datetime.now()
        picking_type_id = picking_return_type_id = self.env['stock.picking.type']
        pickings = self.env['stock.picking']
        vals = {}
        #reason_id = self.env['stock.transfer.close.reason'].search([('reason_type','=',type)],limit=1)
        for order in self:
            #stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_category','=','close'),('stage_code','=','CL')],limit=1)
            if not order.disable_close:
                if order.picking_state:
                    if order.transfer_order_type_id.auto_expiry and order.stage_id.id in (order.transfer_order_type_id.close_allow_on_stage_ids.mapped('id')):
                        if order.order_deadline < fields.Datetime.now():
                            vals = {
                                'stage_id': order.transfer_order_type_id.expiry_stage_id.id, 
                                'date_closed': today,
                                'close_reason_id' : order.transfer_order_type_id.expiry_default_reason_id.id,
                                'close_reason_message' : 'Auto Closed',
                                'last_stage_id': order.stage_id.id,
                                }
                elif order.picking_state == False or not order.picking_state:
                    if order.transfer_order_type_id.auto_reject and order.stage_id.id in (order.transfer_order_type_id.rej_allow_on_stage_ids.mapped('id')):                     
                        if order.delivery_deadline < fields.Datetime.now():
                            vals = {
                                'stage_id': order.transfer_order_type_id.reject_stage_id.id, 
                                'date_closed': today,
                                'close_reason_id' : order.transfer_order_type_id.reject_default_reason_id.id,
                                'close_reason_message' : 'Auto Reject',
                                'last_stage_id': order.stage_id.id,
                            }
                picking_type_id = order.transfer_order_category_id.picking_type_id.id
                picking_return_type_id = order.transfer_order_category_id.return_picking_type_id.id

                order.sudo().write(vals)
                #for picking in pickings.search([('stock_transfer_order_id','=',order.id),('state','!=','done')])
                for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id in (picking_type_id, picking_return_type_id) and p.state not in ('done','cancel')):
                    picking.sudo().action_cancel()
        return type
    
    def _cancel_delivery(self, automatic=False):
        auto_commit = self.env.context.get('auto_commit', True)
        cr = self.env.cr
        picking = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)],limit=1)
        picking.sudo().action_cancel()
        for order in self:
            order.write({
                'close_reason_message' : 'Document expired automatically',
                'date_closed': fields.Date.from_string(fields.Date.context_today(self)),
            })
        cr.commit()
        if auto_commit:
            cr.commit()
    
    @api.depends('picking_ids.state')
    def _compute_picking_state(self):
        for order in self:
            #if order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id):
            if order.picking_ids:
                if all(picking.state not in ('done','cancel') for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)):
                    order.picking_state = 'PK'
                else:
                    if any(picking.state != 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)):
                        order.picking_state = 'PS'
                    elif all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)) and all(picking.state == 'draft' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):
                        order.picking_state = 'FS'
                    elif all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)) and any(picking.state in ('waiting','confirmed','assigned') for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):
                        order.picking_state = 'RT'
                    elif all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)) and all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):
                        order.picking_state = 'CL'
                             
                        #if any(picking.state in ('waiting','confirmed','assigned') for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):
                            #order.picking_state = 'RT'
                        #if all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):
                            #order.picking_state = 'CL'
                        #else:
                            #order.picking_state = 'FS'
            #elif order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id):
                
            #else:
                #order.picking_state = False
                        
    @api.depends('picking_state')
    def _compute_stage_id(self):
        order_type_stage_id = self.env['stock.transfer.picking.status']
        for order in self:
            #order.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_code','=','PK')],limit=1).id
            if not order.close_reason_id:
                order_type_stage_id = self.env['stock.transfer.picking.status'].search([('transfer_order_type_id','=',order.transfer_order_type_id.id),('picking_state','=',order.picking_state)],limit=1)
                order.stage_id = order_type_stage_id.stage_id.id
                #if order.picking_state == 'PK':
                    #order.stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','PK')],limit=1).id
                #elif order.picking_state == 'PS':
                    #order.stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','PS')],limit=1).id
                #elif order.picking_state == 'FS':
                    #order.stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','FS')],limit=1).id
                #elif order.picking_state == 'RT':
                    #order.stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','RT')],limit=1).id
                #elif order.picking_state == 'CL':
                    #order.stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','CL')],limit=1).id
            



                
    @api.depends('picking_ids','picking_ids.state')
    def _compute_stage_id0(self):
        for order in self:
            if order.picking_ids:
                if all(picking.state not in ('done','cancel') for picking in order.picking_ids):
                    #Waiting
                    order.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_code','=','PK')],limit=1).id
                else:
                    if any(picking.state != 'done' for picking in order.picking_ids):
                        #partially Shipped
                        order.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_code','=','PS')],limit=1).id
                    elif all(picking.state == 'done' for picking in order.picking_ids):
                        #fully Shipped
                        order.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_code','=','FS')],limit=1).id
            if not order.stage_id.id:
                order.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_code','=','PK')],limit=1).id
                    
    
    def _stage_find(self, type_id=None, category_id=None, domain=None, order='sequence'):
        if category_id:
            search_domain = [('transfer_order_category_ids', '=', category_id)]
        if domain:
            search_domain += list(domain)
        return self.env['stock.transfer.order.stage'].search(search_domain, order=order, limit=1)
    
    #@api.depends('transfer_order_type_id')
    #def _compute_stage_id(self):
    #    for order in self:
    #        if order.transfer_order_type_id:
    #            if order.transfer_order_type_id not in order.stage_id.transfer_order_type_ids:
                    
    @api.depends('transfer_order_type_id')        
    def _compute_stage_id2(self):
        dlvr_qty = demand_qty = 0
        for order in self:
            if order.transfer_order_type_id:
                if order.transfer_order_type_id not in order.stage_id.transfer_order_type_ids:
                    order.stage_id = order.stage_find(order.transfer_order_type_id.id, [('fold', '=', False), ('stage_category', '=', 'draft')])
                elif order.picking_ids:
                    for line in order.stock_transfer_order_line:
                        demand_qty += line.product_uom_qty
                        dlvr_qty += line.delivered_qty
                    if demand_qty == dlvr_qty:
                        order.stage_id = order.stage_find(order.transfer_order_type_id.id, [('fold', '=', False), ('stage_category', '=', 'draft')])
                    elif dlvr_qty > 0 and dlvr_qty < demand_qty:
                        order.stage_id = order.stage_find(order.transfer_order_type_id.id, [('fold', '=', False), ('stage_category', '=', 'draft')])
            else:
                order.stage_id = False
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        section_ids = category_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('transfer_order_type_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('transfer_order_type_ids', '=', section_id))
        """
        if category_id:
            category_ids.append(category_id)
        category_ids.extend(self.mapped('transfer_order_category_id').ids)
        search_domain = []
        if category_ids:
            search_domain = [('|')] * (len(category_ids) - 1)
            for category_id in category_ids:
                search_domain.append(('transfer_order_category_ids', '=', category_id))
        """       
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['stock.transfer.order.stage'].search(search_domain, order=order, limit=1).id
    
    def _compute_all_txn(self):
        transfer_order_type_id = self.curr_txn_type_id
        stage_id = self.stage_id
        stage = []
        #if self.stock_transfer_txn_line:
            #.sorted(key=lambda r: r.sequence)   
            #for txn in self.stock_transfer_txn_line.filtered(lambda t: t.txn_action == 'open'):
             #   transfer_order_type_id = txn.transfer_exception_type_id
               # break
        self.curr_txn_type_id = transfer_order_type_id
        self.txn_stage_ids = [(6, 0, self.stock_transfer_txn_line.txn_stage_id.ids)]
            #for txn in self.stock_transfer_txn_line.filtered(lambda t: t.txn_action == 'open').sorted(key=lambda r: r.sequence):
             #   stages.append({
              #      'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
               # })
    #@api.onchange('transfer_exception_type_id')
    #def _onchange_transfer_exception_type_id(self):
    #    if self.transfer_exception_type_id.stage_id:
    #        self.stage_id = self.transfer_exception_type_id.stage_id.id

    
        
    #@api.onchange('picking_type_id')
    #def _onchange_picking_type(self):
        #for line in self:
            #line.location_src_id = line.picking_type_id.default_location_src_id
            #line.location_dest_id = line.picking_type_id.default_location_dest_id
    
    @api.onchange('transfer_order_category_id')
    def _onchange_trasnfer_order_category(self):
        if self.transfer_order_category_id:
            self.location_src_id = self.transfer_order_category_id.location_src_id.id
            self.location_dest_id = self.transfer_order_category_id.location_dest_id.id
            self.picking_type_id = self.transfer_order_category_id.picking_type_id.id
            ddays = self.transfer_order_category_id.default_delivery_validity
            ldays = self.transfer_order_category_id.delivery_lead_days
            edays = self.transfer_order_category_id.default_order_validity
            if ddays > 0:
                self.delivery_deadline = fields.Date.to_string(datetime.now() + timedelta(ddays))
                self.order_deadline = fields.Date.to_string(datetime.now() + timedelta(edays))
        

    
    def _compute_all_dates(self):
        ddt = rdt = False
        pickings = self.env['stock.picking']
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id),('picking_type_id','=',order.picking_type_id.id),('state','=','done')])
        for picking in pickings:
            if picking.date_done:
                ddt = picking.date_done
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id),('picking_type_id','=',order.transfer_order_category_id.return_picking_type_id.id),('state','=','done')])
        for picking in pickings:
            if picking.date_done:
                rdt = picking.date_done
        self.date_delivered = ddt
        self.date_returned = rdt
        
    @api.depends('picking_state')
    def _compute_return_deadline(self):  
        dt = False
        days = 0
        for order in self:
            if order.date_delivered:
                days = order.transfer_order_category_id.default_return_validity
                dt = fields.Date.to_string(order.date_delivered + timedelta(days))
        self.return_deadline = dt
    
    def action_draft(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to cancel '%s'.", order.stage_id.name))
        stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('transfer_order_category_ids','=',self.transfer_order_category_id.id)],limit=1)
        self.update({
            'stage_id': stage_id.id,
        })
        for txn in self.stock_transfer_txn_line:
            txn.txn_action = 'open'
            txn.sudo().unlink()
            
    
    def action_confirm(self):
        for order in self.sudo():
            txn_count = self.env['stock.transfer.exception.type'].search_count([('transfer_order_category_ids','=',order.transfer_order_category_id.id),('apply_stage_id','=',order.stage_id.id)])
            if order.stage_id.allow_transactions:
                if txn_count > 0:
                    if len(order.transfer_exception_type_ids.filtered(lambda r: r.apply_stage_id.id == order.stage_id.id)) == 0:
                      raise UserError(_('Please select any of exception on %s') % (order.stage_id.name))
        
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to approve '%s'.", order.stage_id.name))
                    
        #self.sudo().process_txn_stage()
        self.update({
            'stage_id' : self.next_stage_id.id,
            'date_order': fields.Datetime.now(),
            'last_stage_id': self.stage_id.id,
        })
        
    def action_refuse(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to refuse '%s'.", order.stage_id.name))
        stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('transfer_order_category_ids','=',self.transfer_order_category_id.id)],limit=1)
        for txn in self.stock_transfer_txn_line:
            if self.prv_stage_id.id == txn.transfer_exception_type_id.exec_stage_id.id:
                txn.txn_action = 'open'
        if self.prv_stage_id:
            self.update({
                'stage_id' : self.prv_stage_id.id,
                'date_order': fields.Datetime.now(),
            })
    
    def action_special_edit(self):
        if self.stage_id.stage_category in ('close','cancel'):
            self.update({
                'special_edit_mode': False
            })
        else:
            self.update({
                'special_edit_mode': True,
                'is_entry_edited': True
            })
        
    def action_cancel(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to cancel '%s'.", order.stage_id.name))
        stage_id = self.env['stock.transfer.order.stage'].search([('stage_category','=','cancel')],limit=1)
        self.update({
            'stage_id': stage_id.id,
        })
        for txn in self.stock_transfer_txn_line:
            txn.txn_action = 'open'
            txn.sudo().unlink()
            
    def action_draft(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to cancel '%s'.", order.stage_id.name))
        stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('transfer_order_category_ids','=',self.transfer_order_category_id.id),('stage_category','=','draft')],limit=1)
        self.update({
            'stage_id': stage_id.id,
        })
        for txn in self.stock_transfer_txn_line:
            txn.txn_action = 'open'
            txn.sudo().unlink()
            
    def action_submit(self):
        self.ensure_one()
        for order in self.sudo():
            group_id = order.transfer_order_category_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                #if not self.env.user.has_group(self.transfer_order_category_id.group_id.name):
                    raise UserError(_("You are not authorize to submit requisition in category '%s'.", self.transfer_order_category_id.name))
            if not order.stock_transfer_order_line:
                raise UserError(_("You cannot submit requisition '%s' because there is no product line.", self.name))
        #self.sudo().process_txn_stage()
        #self._compute_order_stages()
        self.update({
            'stage_id' : self.next_stage_id.id,
            'last_stage_id': self.stage_id.id,
        })
        
    def process_txn_stage(self):
        exceptions = self.env['stock.transfer.exception.type'].search([('transfer_order_type_id','=',self.transfer_order_type_id.id),('transfer_order_category_id','=',self.transfer_order_category_id.id),('apply_stage_id','=',self.stage_id.id),('stage_auto_apply','=',True)])
        #self.stock_transfer_txn_line.filtered(filtered(lambda mo: mo.state not in ['cancel', 'draft', 'done'])
        for exception in exceptions:
            #self.stock_transfer_txn_line.filtered(filtered(lambda txn: txn.transfer_exception_type_id.id == exception.id).unlink()
            for line in self.stock_transfer_txn_line:
                if line.transfer_exception_type_id.id == exception.id:
                    line.unlink()
            self.env['stock.transfer.txn.line'].create({
                'stock_transfer_order_id': self.id,
                'transfer_exception_type_id': exception.id,
            })

            #if self.stock_transfer_txn_line:
             #   for line in self.stock_transfer_txn_line:
              #      if not line.transfer_exception_type_id.id == exception.id:
               #         self.env['stock.transfer.txn.line'].create({
                #            'stock_transfer_order_id': self.id,
                 #           'transfer_exception_type_id': exception.id,
                  #      })
            #else:
             #   self.env['stock.transfer.txn.line'].create({
              #      'stock_transfer_order_id': self.id,
               #     'transfer_exception_type_id': exception.id, 
                #})
                
        for order in self:
            if order.next_stage_id.id == order.curr_txn_stage_id.id or order.curr_txn_type_id.exec_stage_id.id == order.stage_id.id:
                for txn in self.stock_transfer_txn_line.filtered(lambda t: t.transfer_exception_type_id.id == order.curr_txn_type_id.id):
                    txn.txn_action = 'apply'
                    for line in order.stock_transfer_order_line:
                        if txn.transfer_exception_type_id.location_src_id:
                            line.location_src_id = txn.transfer_exception_type_id.location_src_id.id
                        if txn.transfer_exception_type_id.location_dest_id:
                            line.location_dest_id = txn.transfer_exception_type_id.location_dest_id.id
                    #for line in order.stock_transfer_return_line:
                     #   if txn.transfer_exception_type_id.location_dest_id:
                      #      line.location_dest_id = txn.transfer_exception_type_id.location_dest_id.id
        
            
    
    def create_delivery(self):
        self._create_delivery()
        if self.action_type != 'normal':
            self._create_return()
        self.update({
            'stage_id' : self.next_stage_id.id,
            'date_order': fields.Datetime.now(),
            'picking_state': 'PK',
        })
        #for order in self:
         #   order.stage_id = order.next_stage_id.id,
        #return self.action_subscription_invoice()
        
    def _create_delivery(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        moves_data = []
        lines_data = []
        for order in self:
            for line in order.stock_transfer_order_line:
                lines_data.append([0,0,{
                    #'reference': order.name,
                    'company_id': order.company_id.id,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'origin': order.name,
                    'name': order.name,
                    'date_deadline': order.date_scheduled,
                    'location_id': line.location_src_id.id,
                    'location_dest_id': line.location_dest_id.id,
                    'stock_transfer_order_line_id': line.id,
                }])
        picking.create({
            'picking_type_id':self.picking_type_id.id,
            'partner_id': order.partner_id.id,
            'company_id': order.company_id.id,
            'location_id': self.location_src_id.id,
            'location_dest_id':self.location_dest_id.id,
            'scheduled_date':self.date_scheduled,
            'origin':self.name,
            'stock_transfer_order_id':self.id,
            'state': 'draft',
            'move_lines':lines_data,
        })
        
        return picking
    
    def _create_return(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        origin_picking_id = self.env['stock.picking']
        lines_data = []
        order = False
        Line = False
        origin_picking_id = self.env['stock.picking'].search([('stock_transfer_order_id','=',self.id),('picking_type_id','=',self.picking_type_id.id),('state','!=','cancel')],limit=1)

        for order in self:
            for line in order.stock_transfer_return_line:
                lines_data.append([0,0,{
                    #'reference': order.name,
                    'company_id': order.company_id.id,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'origin': 'return of ' + origin_picking_id.name,
                    'name': order.name,
                    'date_deadline': order.date_scheduled,
                    'location_id': line.location_dest_id.id,
                    'location_dest_id': order.return_location_id.id,
                    'stock_transfer_return_line_id': line.id,
                    'origin_returned_move_id': self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_id','=',origin_picking_id.id)]).id
                }])
            picking.create({
                'picking_type_id':order.transfer_order_category_id.return_picking_type_id.id,
                'partner_id': order.partner_id.id,
                'location_id': order.location_dest_id.id,
                'location_dest_id':order.return_location_id.id,
                'company_id': order.company_id.id,
                'scheduled_date':self.date_scheduled,
                'origin': 'return of ' + origin_picking_id.name,
                'stock_transfer_order_id':self.id,
                'state': 'draft',
                'move_lines':lines_data,
            })
        
        return picking
    
    
    def _compute_picking_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for order in self:
            order.delivery_count = can_read and Picking.search_count([('stock_transfer_order_id', '=', order.id),('picking_type_id', '=', order.picking_type_id.id)]) or 0
            order.return_count = can_read and Picking.search_count([('stock_transfer_order_id', '=', order.id),('picking_type_id', '=', order.transfer_order_category_id.return_picking_type_id.id)]) or 0

    def action_view_delivery(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        pickings = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id)])
        if len(pickings) > 1:
            action['domain'] = [('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id),('state', '!=', 'cancel')]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == self.picking_type_id.id)
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    def action_view_receipt(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        #pickings = self.mapped('picking_ids')
        pickings = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)])
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        
        return action
    
    def _compute_bill_count(self):
        Bill = self.env['account.move']
        can_read = Bill.check_access_rights('read', raise_exception=False)
        for order in self:
            order.bill_count = can_read and Bill.search_count([('stock_transfer_order_id', '=', order.id)]) or 0

    def action_view_credit_note(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Bills',
            'domain': [('stock_transfer_order_id', 'in', self.ids)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }


    """ 
    def action_view_credit_note(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('stock_transfer_order_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    """
    
class StockTransferOrderLine(models.Model):
    _name = 'stock.transfer.order.line'
    _description = 'Stock transfer.order Line'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer.order Order', required=True, ondelete='cascade', index=True, copy=False)
    transfer_order_type_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_type_id', readonly=True, store=True)
    transfer_order_category_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_category_id', readonly=True, store=True)
    stage_id = fields.Many2one(related='stock_transfer_order_id.stage_id', readonly=True,store=True)
    stage_category = fields.Selection(related='stock_transfer_order_id.stage_category', store=True)
    action_type = fields.Selection(related='stock_transfer_order_id.action_type', store=True)
    date_request = fields.Datetime(related='stock_transfer_order_id.date_request', readonly=True)
    date_order = fields.Datetime(related='stock_transfer_order_id.date_order', readonly=True)
    
    partner_id = fields.Many2one('res.partner', related='stock_transfer_order_id.partner_id', readonly=True,store=True)
    user_id = fields.Many2one('res.users', related='stock_transfer_order_id.user_id', readonly=True,store=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict', )
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    categ_control_ids = fields.Many2many(related='stock_transfer_order_id.categ_control_ids')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_qty = fields.Float(string='Demand Qty', required=True)
    
    delivered_qty = fields.Float(string='Dlvr. Qty', copy=False, store=True, compute='_compute_delivered_qty')
    remaining_qty = fields.Float(string='Remainig Qty', copy=False, store=True, compute='_compute_delivered_qty')
    
    date_scheduled = fields.Date(string='Scheduled Date')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    project_id = fields.Many2one('project.project', string='Project')
    location_src_id = fields.Many2one('stock.location', string='From', )
    location_dest_id = fields.Many2one('stock.location', string='To', )
    return_product_id = fields.Many2one('product.product', string='Return Product', compute='_compute_product_return' )
    return_product_uom_qty = fields.Float(string='Return Qty', compute='_compute_product_return')

    
    site_type = fields.Selection([
        ('gbt', 'GBT'), 
        ('rtp', 'RTP'),
    ], string="Site Type", default="gbt")
    tower_height = fields.Float(string='Tower Height')
    kpa = fields.Integer(string='KPA')
    wind_zone = fields.Integer(string='Wind Zone')
    
    
    delivery_status = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')],string="Status", compute="_get_delivery_status")
    
    def unlink(self):
        if self.stock_transfer_order_id.stage_category != 'draft':
            raise UserError(_('You can only delete draft entries.'))
        else:
            res = super(StockTransferOrderLine, self).unlink()
        return res
    
    @api.onchange('project_id')
    def onchange_project_id(self):
        if not self.analytic_account_id:
            self.analytic_account_id = self.project_id.analytic_account_id.id
    
    def _compute_product_return(self):
        for line in self:
            qty = 0
            returns = self.env['stock.transfer.return.line'].search([('stock_transfer_order_id','=',line.stock_transfer_order_id.id),('categ_id','=',line.categ_id.id)])
            for rtn in returns:
                qty += rtn.product_uom_qty
            line.return_product_uom_qty = qty
            line.return_product_id = False
        
    def _get_delivery_status(self):
        #status = ''
        picking_code = ''
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.stage_id.stage_category == 'transfer':
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                else:
                    picking_code = line.stock_transfer_order_id.picking_type_code
            else:
                picking_code = line.stock_transfer_order_id.picking_type_code
            stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
            status = stock_move.state
        self.delivery_status = status
    
    def _get_return_product(self):
        #status = ''
        product_id = False
        picking_code = False
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id:
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                    stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
                    product_id = stock_move.product_id.id
        self.return_product_id = product_id
        
    def _compute_all_qty(self):
        del_qty = rcv_qty = 0
        move_lines = self.env['stock.move']
        for line in self:
            del_qty = rcv_qty = 0
            move_lines = self.env['stock.move'].search([('stock_transfer_order_line_id', '=', line.id),('picking_id.stock_transfer_order_id', '=', line.stock_transfer_order_id.id), ('state', '=', 'done'),('picking_id.picking_type_id','=', line.stock_transfer_order_id.picking_type_id.id)])
            for move in move_lines:
                del_qty += move.quantity_done
                            
            line.update({
                'delivered_qty': del_qty,
                #'received_qty' : 100, #rcv_qty,
            })
    
    @api.depends('stock_transfer_order_id.picking_ids','stock_transfer_order_id.picking_ids.state')
    def _compute_delivered_qty(self):
        for line in self:
            if line.product_id.id:
                stock_move_obj = self.env['stock.move']
                domain = [('stock_transfer_order_line_id', '=', line.id),
                          ('picking_code', '=', line.stock_transfer_order_id.picking_type_code),
                          ('state', '=', 'done'), 
                         ]
                where_query = stock_move_obj._where_calc(domain)
                stock_move_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(product_qty) from " + from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            line.delivered_qty = self.env.cr.fetchone()[0] or 0.0
            line.remaining_qty = line.product_uom_qty - line.delivered_qty
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
            self.location_src_id = self.stock_transfer_order_id.location_src_id.id
            #self.location_dest_id = self.stock_transfer_order_id.location_dest_id.id
        if not self.date_scheduled:
            self.date_scheduled = self.stock_transfer_order_id.date_scheduled
            
    def action_view_transfer_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("action_stock_transfer_order_pending")
        pickings = self.env['stock.transfer.order.order'].search([('id', '=', self.stock_transfer_order_id.id)])
        if len(pickings) > 1:
            action['domain'] = [('id', '=', self.stock_transfer_order_id.id)]
        elif pickings:
            form_view = [(self.env.ref('de_stock_transfer_order.stock_transfer_order_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == self.picking_type_id.id)
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    
class StockTransferReturnLine(models.Model):
    _name = 'stock.transfer.return.line'
    _description = 'Stock transfer Return Line'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer.order Order', required=True, ondelete='cascade', index=True, copy=False)
    partner_id = fields.Many2one('res.partner', related='stock_transfer_order_id.partner_id', readonly=True)
    user_id = fields.Many2one('res.users', related='stock_transfer_order_id.user_id', readonly=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict', )
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    categ_control_ids = fields.Many2many(related='stock_transfer_order_id.categ_control_ids')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_qty = fields.Float(string='Demand Qty', required=True)
    
    received_qty = fields.Float(string='Rcvd. Qty', compute='_compute_received_qty', store=True)
    
    date_scheduled = fields.Date(string='Scheduled Date')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    project_id = fields.Many2one('project.project', string='Project')
    location_src_id = fields.Many2one('stock.location', string='From', )
    location_dest_id = fields.Many2one('stock.location', string='To', )
    return_status = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')],string="Status", compute="_get_delivery_status")
    igt_barcode = fields.Char(string='IGT Barcode')
    oem_barcode = fields.Char(string='OEM Barcode')
    
    def unlink(self):
        if self.stock_transfer_order_id.stage_category != 'draft':
            raise UserError(_('You can only delete draft entries.'))
        else:
            res = super(StockTransferReturnLine, self).unlink()
        return res
    
    @api.depends('stock_transfer_order_id.picking_ids','stock_transfer_order_id.picking_ids.state')
    def _compute_received_qty(self):
        del_qty = rcv_qty = 0
        move_lines = self.env['stock.move']
        for line in self:
            rcv_qty = 0
           
            move_lines = self.env['stock.move'].search([('stock_transfer_return_line_id', '=', line.id),('picking_id.stock_transfer_order_id', '=', line.stock_transfer_order_id.id), ('state', '=', 'done'),('picking_id.picking_type_id','=', line.stock_transfer_order_id.picking_type_id.return_picking_type_id.id)])
            for move in move_lines:
                rcv_qty += move.quantity_done
            
            line.update({
                'received_qty' : rcv_qty,
            })
            
    @api.onchange('product_id')
    def _onchange_return_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
            self.location_dest_id = self.stock_transfer_order_id.location_src_id.id
            self.location_src_id = self.stock_transfer_order_id.location_dest_id.id
        if not self.date_scheduled:
            self.date_scheduled = self.stock_transfer_order_id.date_scheduled
            
    def _get_delivery_status(self):
        #status = ''
        picking_code = ''
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.stage_id.stage_category == 'transfer':
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                else:
                    picking_code = line.stock_transfer_order_id.picking_type_code
            else:
                picking_code = line.stock_transfer_order_id.picking_type_code
            stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
            status = stock_move.state
        self.return_status = status
        
class StockTransferTXNLine(models.Model):
    _name = 'stock.transfer.txn.line'
    _description = 'Stock transfer Transaction Line'
    _order = 'sequence, id'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer order', required=True, ondelete='cascade', index=True, copy=False)
    stage_id = fields.Many2one('stock.transfer.order.stage',related='stock_transfer_order_id.stage_id')
    transfer_order_type_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_type_id', readonly=True, store=True)
    sequence = fields.Integer(default=1, compute='_compute_sequence')
    transfer_exception_type_id = fields.Many2one("stock.transfer.exception.type", string="Exceptions")
    txn_stage_id = fields.Many2one('stock.transfer.order.stage', related='transfer_exception_type_id.stage_id')
    txn_action = fields.Selection([
        ('open', 'Open'),
        ('apply', 'Applied'),
    ], string='Action', copy=False, default='open')
    
    @api.depends('transfer_exception_type_id')
    def _compute_sequence(self):
        for txn in self:
            if txn.transfer_exception_type_id:
                txn.sequence = txn.transfer_exception_type_id.sequence
            else:
                txn.sequence = 0    
  
    def unlink(self):
        if self.txn_action == 'apply':
            raise UserError(_('You cannot delete an applied transaction.'))
        res = super().unlink()
        return res
                
