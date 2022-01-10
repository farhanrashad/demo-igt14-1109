# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class City(models.Model):
    _inherit = 'res.city'

    enforce_districts = fields.Boolean(related='country_id.enforce_districts')
    district_required = fields.Boolean(related='country_id.district_required')
    enforce_subdistricts = fields.Boolean(related='country_id.enforce_subdistricts')
    subdistrict_required = fields.Boolean(related='country_id.subdistrict_required')
    
    district_id = fields.Many2one('res.country.district', string='District', domain="[('state_id', '=', state_id)]")
    subdistrict_id = fields.Many2one('res.country.subdistrict', string='Sub District', domain="[('district_id', '=', district_id)]")