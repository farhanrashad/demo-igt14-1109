# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    allow_picking = fields.Boolean(string="Allow Picking")
    delivery_picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',)
    receipt_picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',)
    is_owner = fields.Boolean(string="Consignment")
