# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import json


class MaterialRequestFormLine(models.Model):
    _name = 'material.request.form.line'
    _description = 'Material Request Form Line Model'
    
    
    name = fields.Char('Reference', related='product_id.default_code')
    product_id = fields.Many2one('product.product', string='Product', domain=[('is_cos_product','=',True)])
    cos_intermediate_entity_id = fields.Char()
    quantity_requested = fields.Float('Qty Requested')
    quantity_prepared = fields.Float('Qty Prepared')
    quantity_to_prepare = fields.Float('Qty To Prepared')
    request_type =  fields.Selection([('1', 'initial'), ('2', 'Remaining'), ('3', 'stock adjustment')], default="1")
    comment =  fields.Char('Comment')
    
    mrf_id = fields.Many2one('material.request.form')
    
    
    




