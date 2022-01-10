# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class PurchaseSubscriptionPlan(models.Model):
    _name = 'purchase.subscription.plan'
    _description = 'Subscription Plan'
    
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    code = fields.Char(help="Code is added automatically in the display name of every subscription.")
    description = fields.Text(translate=True, string="Terms and Conditions")
    recurring_interval_type = fields.Selection([('daily', 'Days'), ('weekly', 'Weeks'),
                                                ('monthly', 'Months'), ('yearly', 'Years'), ],
                                               string='Recurrence', required=True,
                                               help="Invoice automatically repeat at specified interval",
                                               default='monthly')
    recurring_interval_rule = fields.Selection([
        ('unlimited', 'Forever'),
        ('limited', 'Fixed')
    ], string='Duration', default='unlimited')
    recurring_interval = fields.Integer(string="Invoicing Period", help="Repeat every (Days/Week/Month/Year)", required=True, default=1)
    recurring_interval_count = fields.Integer(string="End After", default=1)
    invoicing_mode = fields.Selection([
        ('manual', 'Manually'),
        ('draft', 'Draft'),
        ('validate', 'Validate'),
    ], required=True, default='draft')
    journal_id = fields.Many2one('account.journal', string="Accounting Journal",
                                 domain="[('type', '=', 'purchase')]", company_dependent=True,
                                 check_company=True,
                                 help="If set, subscriptions with this template will invoice in this journal; otherwise the sales journal with the lowest sequence is used.")

    company_id = fields.Many2one('res.company', index=True)
    product_count = fields.Integer(compute='_compute_product_count')
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        for plan in self:
            plan.subscription_count = self.env['purchase.subscription'].search_count([('subscription_plan_id','=',plan.id)])
            
    def _compute_product_count(self):
        product_data = self.env['product.template'].sudo().read_group([('subscription_plan_id', 'in', self.ids)], ['subscription_plan_id'], ['subscription_plan_id'])
        result = dict((data['subscription_plan_id'][0], data['subscription_plan_id_count']) for data in product_data)
        for plan in self:
            plan.product_count = result.get(plan.id, 0)
