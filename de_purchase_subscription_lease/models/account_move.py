# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = "account.move"
    
    la_inv_number = fields.Char(string='Number')
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    purchase_subscription_schedule_id = fields.Many2one("purchase.subscription.schedule")
