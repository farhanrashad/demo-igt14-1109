# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_product_category_power = fields.Boolean(string='Is Category Power?')
    is_product_category_tower = fields.Boolean(string='Is Category Tower?')
    
    wind_factor = fields.Many2one('wind.factor.value', string='Wind Category')
    tower_height = fields.Float(string='Tower Height')

class ProjectProjectInh(models.Model):
    _inherit = 'project.project'
    
    state_id = fields.Many2one('res.country.state', string='Region', domain="[('country_id.name', '=', 'Myanmar')]" )
