# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_subscription_id = fields.Many2one("purchase.subscription")
    subscription_type_id = fields.Many2one("purchase.subscription.type", )
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    purchase_subscription_id = fields.Many2one("purchase.subscription")
    subscription_start_date = fields.Date(
        string="Billing From", readonly=True
    )
    subscription_end_date = fields.Date(
        string="Billing To", readonly=True
    )