# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'
    
    purchase_id = fields.Many2one('purchase.order', string='Purchase', required=False)
    
    def action_approve(self):
        request = super(ApprovalRequest, self).action_approve()
        purchase = self.env['purchase.order']
        if self.request_status == 'approved':
            purchase = self.env['purchase.order'].browse(self.purchase_id.id)
            purchase.approval_state = 'approved'
        
class ApprovalApprover(models.Model):
    _inherit = 'approval.approver'
    
    purchase_id = fields.Many2one(related='request_id.purchase_id')
    
    def action_view_request(self):
        action = self.env["ir.actions.actions"]._for_xml_id("approvals.approval_request_action_all")
        requests = self.request_id
        if len(requests) > 1:
            action['domain'] = [('id', 'in', requests.ids)]
        elif requests:
            form_view = [(self.env.ref('approvals.approval_request_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = requests.id
        return action