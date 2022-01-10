# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockTransferCloseReason(models.Model):
    _name = "stock.transfer.close.reason"
    _order = "sequence, id"
    _description = "Stock Transfer Close Reason"

    name = fields.Char('Reason', required=True, translate=True)
    sequence = fields.Integer(default=10)
    stage_id = fields.Many2one('stock.transfer.order.stage', string='Close Stage')
