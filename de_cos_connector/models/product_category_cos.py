# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductCategoryCOS(models.Model):
    _name = 'product.category.cos'
    
    name = fields.Char('Category Name', required=True)
    cos_category_id = fields.Char('COS Category ID')
    
    
    
class ProductManufacturerCOS(models.Model):
    _name = 'product.manufacturer.cos'
    
    name = fields.Char('Manufacturer Name', required=True)
    cos_manufacturer_id = fields.Char('COS Manufacturer ID')
    
