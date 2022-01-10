# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'
    
    vendor_pricelist_ids = fields.One2many('product.supplierinfo', 'project_id', string='Pricelist', copy=False, auto_join=True,)