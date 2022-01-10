# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockRefill(models.Model):
    _name = 'stock.refill'
    _description = 'Stock Refill'
    
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    refill_date = fields.Datetime(string='Refill Date', required=True, readonly=True, states={'draft': [('readonly', False)]},)
    company_id = fields.Many2one('res.company', store=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(
        'res.users', 'Responsible', tracking=True,
        domain=lambda self: [('groups_id', 'in', self.env.ref('stock.group_stock_user').id)],
        default=lambda self: self.env.user, readonly=True, states={'draft': [('readonly', False)]},)

    location_src_id = fields.Many2one('stock.location', string="Src. Location", required=True, domain="[('usage','=','internal')]")
    location_dest_id = fields.Many2one('stock.location', string="Dest. Location", required=True, domain=[('usage','=','inventory')])
    owner_id = fields.Many2one('res.partner', string="Owner", readonly=True, states={'draft': [('readonly', False)]},)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('inprocess', 'In-Filling'),
            ('done', 'Refilled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft', )
    refill_line_ids = fields.One2many('stock.refill.line', 'stock_refill_id', string="Refilling Line", readonly=True, states={'draft': [('readonly', False)]},)
    transfer_count = fields.Integer(compute='_compute_transfer_count', string="Transfer Count")
    total_available_qty = fields.Float(compute='_all_available_quantity', string="Available Qunatity")
    total_filled_qty = fields.Float(compute='_all_filled_quantity', string="Filled Qunatity")
    
    @api.depends('refill_line_ids.stock_move_qty')
    def _compute_state(self):
        picking = self.env['stock.picking'].search([('stock_refill_id', '=', self.id)],limit=1)
        if picking or len(picking):
            if picking.state not in ('done','cancel'):
                self.state = 'inprocess'
            elif picking.state == 'done':
                self.state = 'done'
        if not self.state:
            self.state = 'draft'
        
    @api.depends('refill_line_ids.product_id','refill_line_ids.location_id')
    def _all_available_quantity(self):
        quants = self.env['stock.quant']
        qty = 0
        for line in self.refill_line_ids:
            quants = self.env['stock.quant'].search([('location_id','in',[line.location_id.id, self.location_src_id.id]),('product_id','=',line.product_id.id)])
            for quant in quants:
                qty += quant.available_quantity
        self.update({
            'total_available_qty': qty
        })
        
    @api.depends('refill_line_ids.product_uom_qty')
    def _all_filled_quantity(self):
        qty = 0
        for line in self.refill_line_ids:
            qty += line.product_uom_qty
        self.update({
            'total_filled_qty': qty
        })
    
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'refill_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['refill_date']))
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.refill', sequence_date=seq_date) or _('New')
        result = super(StockRefill, self).create(vals)       
        return result
    
    def action_validate(self):
        pickings = self.env['stock.picking'].search([('stock_refill_id', '=', self.id),('state','not in',['done','cancel'])])
        for picking in pickings:
            picking.sudo().action_confirm()
            picking.sudo().button_validate()
            
    def action_confirm(self):
        picking = self.env['stock.picking']
        picking_type_id = self.env['stock.picking.type'].search([('company_id', '=', self.company_id.id), ('code', '=', 'internal')], limit=1)

        lines_data = []
        for line in self.refill_line_ids:
            lines_data.append([0,0,{
                'name': line.product_id.name + 'Refilled in ' + line.location_id.name,
                #'reference': ,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'product_uom_qty': line.product_uom_qty,
                'quantity_done': line.product_uom_qty,
                'location_id': line.location_id.id,
                'location_dest_id': line.location_dest_id.id,
                'stock_refill_line_id': line.id,
               
            }])
        picking.create({
            'stock_refill_id': self.id,
            'picking_type_id': picking_type_id.id,
            #'name': self.name,
            'company_id': self.company_id.id,
            'user_id': self.user_id.id,
            'owner_id': self.owner_id.id,
            #'partner_id': self.partner_id.id,
            'location_id': self.location_src_id.id,
            'location_dest_id': self.location_dest_id.id,
            'date': self.refill_date,
            'date_deadline': self.refill_date,
            'scheduled_date': self.refill_date,
            'state': 'draft',
            'move_type':'direct',
            'origin':self.name,
            'move_lines':lines_data,
        })
        
        
    def action_done(self):
        self.state = 'done'
        
    def _compute_transfer_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for refill in self:
            refill.transfer_count = can_read and Picking.search_count([('stock_refill_id', '=', refill.id)]) or 0
            
    def action_transfer_consumption(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search([('stock_refill_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_form")
        action["context"] = {
            "create": False,
            "default_picking_type_code": "internal"
        }
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    
    class StockRefillLine(models.Model):
        _name = 'stock.refill.line'
        _description = 'Stock Refill Entry Line'
        
        stock_refill_id = fields.Many2one('stock.refill' , string="Stock Refill line")
        location_id = fields.Many2one('stock.location' , string="From", required=True, domain=[('is_refilling','=',True)])
        storage_capacity = fields.Float(related='location_id.storage_capacity')
        location_dest_id = fields.Many2one('stock.location' , related='stock_refill_id.location_dest_id')
        product_id = fields.Many2one(related='location_id.product_id')
        product_uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
        current_quantity = fields.Float(string='Current Quantity')
        product_uom_qty = fields.Float(string='Refill Qty')
        closing_quantity = fields.Float(string='Closing Quantity')
        stock_move_qty = fields.Float(string='Confirmed Qty', compute='_move_confirmed_quantity')
        
        @api.depends('stock_refill_id.state')
        def _move_confirmed_quantity(self):
            qty = 0
            move_lines = self.env['stock.move']
            for line in self:
                move_lines = self.env['stock.move'].search([('stock_refill_line_id', '=', line.id),('state', '=', 'done')])
                for move in move_lines:
                    qty += move.quantity_done
                line.update({
                    'stock_move_qty': qty
                })
        
        
        
        
    
    
    
    

