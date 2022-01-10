# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, models, fields
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit = 'res.partner'
    
    country_enforce_towns = fields.Boolean(related='country_id.enforce_towns', readonly=True)
    town_id = fields.Many2one('res.city.town', string='Township', )
    
    enforce_districts = fields.Boolean(related='country_id.enforce_districts')
    enforce_subdistricts = fields.Boolean(related='country_id.enforce_subdistricts')
    
    district_id = fields.Many2one('res.country.district', related='town_id.city_id.district_id')
    subdistrict_id = fields.Many2one('res.country.subdistrict', related='town_id.city_id.subdistrict_id')
    
    @api.depends('city_id')
    def _get_town_district(self):
        for partner in self:
            if partner.enforce_districts:
                partner.district_id = partner.city_id.district_id.id
        if not self.district_id:
            self.district_id = False
        if not self.subdistrict_id:
            self.subdistrict_id = False
        

