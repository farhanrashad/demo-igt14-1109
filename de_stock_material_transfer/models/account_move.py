# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    stock_transfer_order_id = fields.Many2one("stock.transfer.order")