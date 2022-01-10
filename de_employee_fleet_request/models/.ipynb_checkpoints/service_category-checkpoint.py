# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    
class ServiceCategoryInherit(models.Model):
    _inherit = 'fleet.service.type'
    
    category = fields.Integer(default=0)
    
    category_id = fields.Many2many('service.category', string='Category')