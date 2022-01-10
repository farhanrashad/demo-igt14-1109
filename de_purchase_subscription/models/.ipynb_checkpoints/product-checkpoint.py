# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    purchase_subscription = fields.Boolean('Purchase Subscription',
        help='If set, confirming a sale order with this product will create a subscription')
    subscription_plan_id = fields.Many2one(
        'purchase.subscription.plan', 'Subscription Plan',
        help="Product will be included in a selected plan")

