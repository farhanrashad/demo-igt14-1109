# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class PurchaseSubscriptionStage(models.Model):
    _inherit = 'purchase.subscription.stage'

    subscription_type_id = fields.Many2one('purchase.subscription.type', string='Subscription Type', required=True, help="The subscription type categories agreement.",)
    
    group_id = fields.Many2one('res.groups', string='Security Group')