# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TransferType(models.Model):
    _inherit = 'stock.transfer.order.type'

    website_published = fields.Boolean(string='Publish on Website')
    
class TransferOrder(models.Model):
    _inherit = 'stock.transfer.order'
    
    
    is_entry_edited = fields.Boolean(string='Portal Entry Editable')




class ExceptionType(models.Model):
    _inherit = 'stock.transfer.exception.type'


class StageLines(models.Model):
    _inherit = 'stock.transfer.order.stage.line'


class TransferStage(models.Model):
    _inherit = 'stock.transfer.order.stage'


class TransferTxnLine(models.Model):
    _inherit = 'stock.transfer.txn.line'