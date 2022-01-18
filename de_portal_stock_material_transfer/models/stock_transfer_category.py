# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TransferCategory(models.Model):
    _inherit = 'stock.transfer.order.category'

    website_published = fields.Boolean(string='Publish on Website')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

class StockTransferReturnLine(models.Model):
    _inherit = 'stock.transfer.return.line'

class ResPartner(models.Model):
    _inherit = 'res.partner'

class ResUser(models.Model):
    _inherit = 'res.users'

class ProjectProject(models.Model):
    _inherit = 'project.project'


class TransferOrder(models.Model):
    _inherit = 'stock.transfer.order'
    
    is_stock_submit_material = fields.Boolean(string='Material Submitted')

class TransferOrderLine(models.Model):
    _inherit = 'stock.transfer.order.line'

class TransferType(models.Model):
    _inherit = 'stock.transfer.order.type'