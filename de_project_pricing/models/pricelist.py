# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'
    
    project_id = fields.Many2one('project.project', string='Project',)