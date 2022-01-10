# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    
    category_id = fields.Many2one('approval.category', related='type_id.category_id', string="Category", required=False)

    approval_state = fields.Selection([
        ('new', 'Draft'),
        ('pending', 'In Approval'),
        ('approved', 'Approved')
    ],default='new')

    approval_request_id = fields.Many2one('approval.request', string='Approval Request', copy=False, readonly=True)
    request_status = fields.Selection(related='approval_request_id.request_status')
    approvers_count = fields.Integer(compute='_compute_approvers_count')

    def _compute_approvers_count(self):
        Approvers = self.env['approval.approver']
        can_read = Approvers.check_access_rights('read', raise_exception=False)
        for requisition in self:
            requisition.approvers_count = can_read and Approvers.search_count([('requisition_id', '=', requisition.id)]) or 0
        
    def action_submit(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("You cannot submit '%s' because there is no product line.", self.name))
        if self.type_id.quantity_copy == 'none' and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot submit the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot submit the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            #self.write({'state': 'ongoing'})
        #else:
            #self.write({'state': 'in_progress'})
        # Set the sequence number regarding the requisition type        
        if self.name == 'New':
            if self.is_quantity_copy != 'none':
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.tender')
            else:
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.blanket.order')
        
        approver_ids  = []
        request_list = []
        for requisition in self:
            request_list.append({
                'name': requisition.name,
                'request_owner_id': requisition.user_id.id,
                'category_id': requisition.category_id.id,
                'requisition_id': requisition.id,
                'reason': requisition.user_id.name + ' Has requested ' + requisition.name + ' for approval.' ,
                'request_status': 'new',
            })
            approval_request_id = self.env['approval.request'].create(request_list)
            approval_request_id._onchange_category_id()
            approval_request_id.action_confirm()
            requisition.approval_request_id = approval_request_id.id
        self.approval_state = 'pending'
