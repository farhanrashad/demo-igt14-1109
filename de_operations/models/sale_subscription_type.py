# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class SaleSubscriptionAgreementType(models.Model):
    _name = 'sale.subscription.agreement.type'
    _description = 'Sale Subscription Type'
    _order = 'id'

    name = fields.Char(string='Name', required=True, translate=True)