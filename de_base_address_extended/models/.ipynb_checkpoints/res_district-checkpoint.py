# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CountryDistrict(models.Model):
    _name = 'res.country.district'
    _description = 'District'
    _order = 'name'

    name = fields.Char("Name", required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', required=True, domain="[('country_id', '=', country_id)]")
    
class CountrySubDistrict(models.Model):
    _name = 'res.country.subdistrict'
    _description = 'District'
    _order = 'name'

    name = fields.Char("Name", required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', required=True, domain="[('country_id', '=', country_id)]")
    district_id = fields.Many2one('res.country.district', string='District', required=True, domain="[('state_id', '=', state_id)]")