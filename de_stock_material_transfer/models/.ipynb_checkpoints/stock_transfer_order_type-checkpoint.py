# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from random import randint


class StockTransferOrderType(models.Model):
    _name = "stock.transfer.order.type"
    _description = "Transfer Order Type"

    def _get_default_image(self):
        default_image_path = get_module_resource('de_stock_material_transfer', 'static/description', 'requisition.png')
        return base64.b64encode(open(default_image_path, 'rb').read())
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', size=3, required=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the transfer type without removing it.")
    description = fields.Text("Requirements", help="Enter here the details of transfer type.")
    disallow_staging = fields.Boolean(string='Disallow Staging')
    image = fields.Binary(string='Image')
    color = fields.Integer(string='Color Index')
    automated_sequence = fields.Boolean('Automated Sequence?',
        help="If checked, the Approval Requests will have an automated generated name based on the given code.")
    sequence_code = fields.Char(string="Sequence Code")
    
    group_id = fields.Many2one('res.groups', string='Security Group')

    #kanban counts
    partially_shipped_count = fields.Integer("Number of Partially Shipped Requisitions", compute="_compute_all_requisitions_count")
    fully_shipped_count = fields.Integer("Number of Fully Shipped Requisitions", compute="_compute_all_requisitions_count")
    open_orders_count = fields.Integer("Number of Open Requisitions", compute="_compute_all_requisitions_count")
    pending_orders_count = fields.Integer("Number of Pending Requisitions", compute="_compute_all_requisitions_count")

    stock_transfer_status_line = fields.One2many('stock.transfer.picking.status', 'transfer_order_type_id', string='Order Status Line', copy=False, auto_join=True,)

    
    #******************Rejection and Auto Close
    auto_expiry = fields.Boolean(string='Enable Auto Expiry', default=False, help='Enable auto expiery of the document.')
    auto_reject = fields.Boolean(string='Enable Auto Rejection', default=False, help='Enable auto rejection of the document.')
    expiry_stage_id = fields.Many2one('stock.transfer.order.stage', string='Expiry Stage')
    reject_stage_id = fields.Many2one('stock.transfer.order.stage', string='Rejection Stage')
    expiry_default_reason_id = fields.Many2one('stock.transfer.close.reason', string='Default Expiry Reason')
    reject_default_reason_id = fields.Many2one('stock.transfer.close.reason', string='Default Reject Reason')
    
    rej_allow_on_stage_ids = fields.Many2many('stock.transfer.order.stage', 'transfer_order_type_rej_stage_rel', 'transfer_order_stage_id', 'transfer_order_type_id', string='Allow auto rejection on stages', )
    close_allow_on_stage_ids = fields.Many2many('stock.transfer.order.stage', 'transfer_order_type_close_stage_rel', 'transfer_order_stage_id', 'transfer_order_type_id', string='Allow auto close on stages', )


    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "type name already exists!"),
    ]
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence',
        copy=False, check_company=True)
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    
    @api.model
    def create(self, vals):
        if vals.get('sequence_code'):
            sequence = self.env['ir.sequence'].create({
                'name': _('Sequence') + ' ' + vals['sequence_code'],
                'padding': 5,
                'prefix': vals['sequence_code'],
                'company_id': vals.get('company_id'),
            })
            vals['sequence_id'] = sequence.id

        transfer_type = super().create(vals)
        return transfer_type

    def write(self, vals):
        if 'sequence_code' in vals:
            for transfer_type in self:
                sequence_vals = {
                    'name': _('Sequence') + ' ' + vals['sequence_code'],
                    'padding': 5,
                    'prefix': vals['sequence_code'],
                }
                if transfer_type.sequence_id:
                    transfer_type.sequence_id.write(sequence_vals)
                else:
                    sequence_vals['company_id'] = vals.get('company_id', transfer_type.company_id.id)
                    sequence = self.env['ir.sequence'].create(sequence_vals)
                    transfer_type.sequence_id = sequence
        if 'company_id' in vals:
            for transfer_type in self:
                if transfer_type.sequence_id:
                    transfer_type.sequence_id.company_id = vals.get('company_id')
        return super().write(vals)
    
    def _compute_all_requisitions_count(self):
        Requisition = self.env['stock.transfer.order']
        can_read = Requisition.check_access_rights('read', raise_exception=False)
        ps_stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','PS')],limit=1)
        fs_stage_id = self.env['stock.transfer.order.stage'].search([('stage_code','=','FS')],limit=1)
        for ot in self:
            ot.partially_shipped_count = can_read and Requisition.search_count([('transfer_order_type_id', '=', ot.id),('stage_code', '=', 'PS')]) or 0
            ot.fully_shipped_count = can_read and Requisition.search_count([('transfer_order_type_id', '=', ot.id),('stage_code', '=', 'FS')]) or 0
            ot.open_orders_count = can_read and Requisition.search_count([('transfer_order_type_id', '=', ot.id),('stage_category', 'not in', ['draft','close','cancel'])]) or 0
            ot.pending_orders_count = can_read and Requisition.search_count([('transfer_order_type_id', '=', ot.id),('stage_category', '=', ['progress'])]) or 0



            
    def create_requisition(self):
        self.ensure_one()
        # If category uses sequence, set next sequence as name
        # (if not, set category name as default name).
        if self.automated_sequence:
            name = self.sequence_id.next_by_id()
        else:
            name = self.name
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.transfer.order",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': name,
                'default_transfer_order_type_id': self.id,
                'default_user_id': self.env.user.id,
            },
        }
    
class StockTransferStatus(models.Model):
    _name = 'stock.transfer.picking.status'
    _description = 'Transfer Picking Status'
    
    transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string='Order Type', required=True, ondelete='cascade', index=True, copy=False)
    stage_id = fields.Many2one('stock.transfer.order.stage', string='Transfer Stage')
    picking_state = fields.Selection([
        ('PK', 'Pickup Delivery'),
        ('PS', 'Partially Shipped'),
        ('FS', 'Fully Shipped'),
        ('RT', 'Ready For Transfer'),
        ('CL', 'Close'),
    ], string='Picking Status', copy=False, )
