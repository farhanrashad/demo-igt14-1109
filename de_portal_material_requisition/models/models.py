# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockTransferOrder(models.Model):
    _inherit = 'stock.transfer.order'


class ResPartner(models.Model):
    _inherit = 'res.partner'


class StockTransferOrder(models.Model):
    _inherit = 'stock.transfer.order.stage'


