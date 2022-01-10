# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def generate_product_barcode(self):
        for line in self:
            if not line.barcode:
                barcode = self.env['ir.sequence'].next_by_code('product.barcode')
                line.update({
                    'barcode' : barcode,
                })
            

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    def generate_variant_barcode(self):
        for line in self:
            if not line.barcode:
                barcode = self.env['ir.sequence'].next_by_code('product.barcode')
                line.update({
                    'barcode' : barcode,
                })
                
           
            
            