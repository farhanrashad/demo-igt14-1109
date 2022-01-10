# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class SaleSubscriptionStage(models.Model):
    _inherit = 'sale.subscription.agreement.stage'

    subscription_type_id = fields.Many2one('sale.subscription.agreement.type', string='Subscription Type',
                                           required=True, help="The subscription type categories agreement.",)