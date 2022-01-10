# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'
    
    move_id = fields.Many2one('account.move', string='Account Move', required=False)
    
    def action_approve(self):
        request = super(ApprovalRequest, self).action_approve()
        move = self.env['account.move']
        if self.request_status == 'approved':
            move = self.env['account.move'].browse(self.purchase_demand_id.id)
            move.sudo().action_post()
            move.approval_state = 'approved'
        
class ApprovalApprover(models.Model):
    _inherit = 'approval.approver'
    
    move_id = fields.Many2one(related='request_id.move_id')
    
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