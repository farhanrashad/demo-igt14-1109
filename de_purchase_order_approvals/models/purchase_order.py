# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    
    order_type_id = fields.Many2one('purchase.order.type', string="Order Type", required=True)
    category_id = fields.Many2one('approval.category', related='order_type_id.category_id', string="Category", required=False)

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
        for purchase in self:
            purchase.approvers_count = can_read and Approvers.search_count([('purchase_id', '=', purchase.id)]) or 0
        
    def action_submit(self):
        approver_ids  = []
        request_list = []
        for purchase in self:
            request_list.append({
                'name': purchase.name,
                'request_owner_id': purchase.user_id.id,
                'category_id': purchase.category_id.id,
                'purchase_id': purchase.id,
                'reason': purchase.user_id.name + ' Has requested ' + purchase.name + ' for approval.' ,
                'request_status': 'new',
            })
            approval_request_id = self.env['approval.request'].create(request_list)
            approval_request_id._onchange_category_id()
            approval_request_id.action_confirm()
            purchase.approval_request_id = approval_request_id.id
        self.approval_state = 'pending'
