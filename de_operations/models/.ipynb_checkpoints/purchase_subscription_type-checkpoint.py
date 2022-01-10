# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class PurchaseSubscriptionType(models.Model):
    _name = 'purchase.subscription.type'
    _description = 'Purchase Subscription Type'
    _order = 'id'

    name = fields.Char(string='Name', required=True, translate=True)