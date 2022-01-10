# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Country(models.Model):
    _inherit = 'res.country'

    enforce_districts = fields.Boolean(
        string='Enforce Districts',
        help="Check this box to ensure every address created in that country has a 'District' chosen "
             "in the list of the country's cities.")
    district_required = fields.Boolean('District Required')
    enforce_subdistricts = fields.Boolean(
        string='Enforce Sub Districts',
        help="Check this box to ensure every address created in that country has a 'Sub District' chosen "
             "in the list of the country's cities.")
    subdistrict_required = fields.Boolean('Sub District Required')
    
    enforce_towns = fields.Boolean(
        string='Enforce Towns',
        help="Check this box to ensure every address created in that country has a 'town or township' chosen "
             "in the list of the country's cities.")
    town_required = fields.Boolean('Township Required')