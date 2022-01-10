# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class PurchaseSubscription(models.Model):
    _inherit = 'purchase.subscription'    
    
    purchase_subscription_msa_line = fields.One2many('purchase.subscription.msa.line', 'purchase_subscription_id', string='Related MSA', copy=False)
    
class PurchaseSubscriptionMSALine(models.Model):
    _name = 'purchase.subscription.msa.line'
    _description = 'Purchase Subscription MSA Line'
    
    purchase_subscription_id = fields.Many2one('purchase.subscription', string='Subscription', ondelete='cascade')
    msa_id = fields.Many2one('master.service.agreement', string='MSA', ondelete='cascade')
    active_billing = fields.Boolean(string="Active for Billing")