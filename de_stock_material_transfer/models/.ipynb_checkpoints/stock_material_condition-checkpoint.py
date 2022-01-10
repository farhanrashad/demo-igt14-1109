# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockTransferMaterialCondition(models.Model):
    _name = "stock.transfer.material.condition"
    _description = "Material Condition"

    name = fields.Char('Name', required=True)
    is_default = fields.Boolean('Default Condition')