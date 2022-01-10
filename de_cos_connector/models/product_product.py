# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductProductInh(models.Model):
    _inherit = 'product.product'
    
    is_cos_product = fields.Boolean('Is COS Product?')
    cos_entity_id = fields.Char('COS Entity ID')
    cos_categ_id = fields.Many2one('product.category.cos', string='COS Category')
    cos_manufact_id = fields.Many2one('product.manufacturer.cos', string='COS Manufacturer')
    
    @api.model
    def create(self, vals):
        if vals['is_cos_product'] == True:
            default_code = vals['default_code'].strip().lower()
            sql = """ select lower(default_code) from product_product where lower(default_code)='""" +str(default_code)+"""' """
            self.env.cr.execute(sql)
            exists = self.env.cr.fetchone()
             
            if exists:
                raise UserError(('A Product already exists with the same Internal Reference!'))
            else:
                pass

        rec = super(ProductProductInh, self).create(vals)
#         print('rec.cos_entity_id',rec.cos_entity_id)
#         raise UserError(rec.cos_entity_id)
        if rec.is_cos_product == True and rec.cos_entity_id == False:
            part_number = rec.default_code
            designation = rec.name
            category = rec.cos_categ_id.cos_category_id
            manufacturer_bis = rec.cos_manufact_id.cos_manufacturer_id
            product_cos = self.env['cos.master'].create_product_on_cos(part_number, designation, category, manufacturer_bis)
            
            rec.cos_entity_id = product_cos['id']
        
        return rec
    
    
