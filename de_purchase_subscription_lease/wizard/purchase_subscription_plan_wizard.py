# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class PurchaseSubscriptionPlanWizard(models.Model):
    _name = 'purchase.subscription.plan.wizard'
    _description = 'Purchase Subscription Plan Wizard'
    
    amount = fields.Float('Escalation %', digits='Account', help="The percentage of amount to be Billed in advance, taxes excluded.")
    #currency_id = fields.Many2one('res.currency', string='Currency')
    purchase_subscription_id = fields.Many2one('purchase.subscription','Subscription',)
    recurring_interval = fields.Integer(string="Invoicing Period", help="Repeat every (Days/Week/Month/Year)", required=True, default=1, tracking=True)
    recurring_interval_type = fields.Selection([('daily', 'Days'), ('weekly', 'Weeks'),
                                                ('monthly', 'Months'), ('yearly', 'Years'), ],
                                               string='Recurrence', required=True, 
                                               help="Invoice automatically repeat at specified interval", default='yearly', tracking=True)
    
    
    
    def create_payment_schedule(self):
        
        subscription_schedule_id = self.env['purchase.subscription.schedule']
        subscription = self.env['purchase.subscription'].browse(self._context.get('active_ids',[]))
        lines_data = {}
        esclation = a_esclation = 0
        interval = 0
        escalation_amount = 0
        
        date_from = date_to = fields.Date.today()
        
        if subscription.stage_id.stage_category == 'draft':
            if subscription.purchase_subscription_schedule_line:
                subscription.purchase_subscription_schedule_line.unlink()
            
            if self.recurring_interval_type == 'yearly':
                escalation_amount = subscription.amount_lease_original #subscription.recurring_price
                for plan in subscription.subscription_plan_id.subscription_plan_schedule_ids: 
                    if (interval % (self.recurring_interval*12)) == 0 and not interval == 0:
                        escalation = self.amount
                        escalation_amount = escalation_amount + (escalation_amount * (escalation/100))
                    else:
                        escalation = 0
                        
                    a_esclation += escalation
                    date_from = subscription.date_start + relativedelta(months=interval)#fields.Date.to_string(subscription.date_start + timedelta(interval))
                    date_to = date_from + relativedelta(months=plan.recurring_interval,days=-1)
                    lines_data = {
                        'purchase_subscription_id': subscription.id,
                        'date_from': date_from,
                        'date_to': date_to,
                        'recurring_price': subscription.amount_lease_original,#subscription.recurring_price,
                        'recurring_intervals': plan.recurring_interval,
                        'discount': 0,
                        'escalation':  escalation,
                        'accum_escalation': a_esclation,
                        'escalation_amount': escalation_amount,
                    }
                    interval += plan.recurring_interval
                    #subscription.purchase_subscription_schedule_line.sudo().create(lines_data)
                    subscription_schedule_id.create(lines_data)
                    #return subscription_schedule_id
                
    
    

class SubscriptionPlanLineWizard(models.TransientModel):
    _name = 'purchase.subscription.plan.line.wizard'
    _description = "Subscription Plan Line Wixard"
    
    wizard_subscription_plan_id = fields.Many2one('purchase.subscription.plan.wizard')
    date_from = fields.Date(string='Date From', readonly=True)
    date_to = fields.Date(string='Date To', readonly=True)
    recurring_price = fields.Float(string="Recurring Price", required=True, readonly=True)
    recurring_intervals = fields.Integer(string="Intervals", required=True, readonly=True)


