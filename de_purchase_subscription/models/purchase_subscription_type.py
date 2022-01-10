# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

class PurchaseSubscriptionType(models.Model):
    _name = 'purchase.subscription.type'
    _description = 'Purchase Subscription Type'
    _order = 'id'
    
    def _get_default_image(self):
        default_image_path = get_module_resource('de_purchase_subscription', 'static/src/img', 'subscription.png')
        return base64.b64encode(open(default_image_path, 'rb').read())

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Char(string="Description", translate=True)
    label_types = fields.Char(string='Use Types as', default='Subscription', help="Label used for the subscriptions of the types.", translate=True)

    image = fields.Binary(string='Image', default=_get_default_image)
    color = fields.Integer(string='Color Index')
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    automated_sequence = fields.Boolean('Automated Sequence?',
        help="If checked, the Approval Requests will have an automated generated name based on the given code.")
    sequence_code = fields.Char(string="Code")
    sequence_id = fields.Many2one('ir.sequence', string='Reference Sequence',
        copy=False, check_company=True)
    
    running_subscription_count = fields.Integer("Number of running subscriptions", compute="_compute_running_subscriptions_count")
    draft_bill_count = fields.Integer("Number of draft bills", compute="_compute_all_bills_count")
    posted_bill_count = fields.Integer("Number of bills", compute="_compute_all_bills_count")

    request_to_validate_count = fields.Integer("Number of requests to validate", compute="_compute_request_to_validate_count")
    
    group_id = fields.Many2one('res.groups', string='Security Group')
    
    def _compute_request_to_validate_count(self):
        for category in self:
            category.request_to_validate_count = 1
            
    def _compute_running_subscriptions_count(self):
        Subscription = self.env['purchase.subscription']
        can_read = Subscription.check_access_rights('read', raise_exception=False)
        for sub in self:
            sub.running_subscription_count = can_read and Subscription.search_count([('subscription_type_id', '=', sub.id),('stage_category', '=', 'progress')]) or 0
    
    def _compute_all_bills_count(self):
        Bill = self.env['account.move']
        can_read = Bill.check_access_rights('read', raise_exception=False)
        for sub in self:
            sub.draft_bill_count = can_read and Bill.search_count([('subscription_type_id', '=', sub.id),('state', '=', 'draft')]) or 0
            sub.posted_bill_count = can_read and Bill.search_count([('subscription_type_id', '=', sub.id),('state', '=', 'posted')]) or 0
            
            
    @api.model
    def create(self, vals):
        if vals.get('automated_sequence'):
            sequence = self.env['ir.sequence'].create({
                'name': _('Sequence') + ' ' + vals['sequence_code'],
                'padding': 5,
                'prefix': vals['sequence_code'],
                'company_id': vals.get('company_id'),
            })
            vals['sequence_id'] = sequence.id

        purchase_subscription_type = super().create(vals)
        return purchase_subscription_type

    def write(self, vals):
        if 'sequence_code' in vals:
            for purchase_subscription_type in self:
                sequence_vals = {
                    'name': _('Sequence') + ' ' + vals['sequence_code'],
                    'padding': 5,
                    'prefix': vals['sequence_code'],
                }
                if purchase_subscription_type.sequence_id:
                    purchase_subscription_type.sequence_id.write(sequence_vals)
                else:
                    sequence_vals['company_id'] = vals.get('company_id', purchase_subscription_type.company_id.id)
                    sequence = self.env['ir.sequence'].create(sequence_vals)
                    purchase_subscription_type.sequence_id = sequence
        if 'company_id' in vals:
            for purchase_subscription_type in self:
                if purchase_subscription_type.sequence_id:
                    purchase_subscription_type.sequence_id.company_id = vals.get('company_id')
        return super().write(vals)    
            
    def create_request(self):
        self.ensure_one()
        # If category uses sequence, set next sequence as name
        # (if not, set category name as default name).
        if self.automated_sequence:
            name = self.sequence_id.next_by_id()
        else:
            name = self.name
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.subscription",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': name,
                'default_subscription_type_id': self.id,
                'default_user_id': self.env.user.id,
            },
        }