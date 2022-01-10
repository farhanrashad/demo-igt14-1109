# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CityTown(models.Model):
    _name = 'res.city.town'
    _description = 'Townships'
    _order = 'name'

    name = fields.Char("Name", required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    city_id = fields.Many2one(
        'res.city', 'City', required=True, domain="[('country_id', '=', country_id)]")