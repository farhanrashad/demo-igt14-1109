# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_team_id = fields.Many2one(
        'purchase.team', 'Purchases Team',
        help='If set, this Purchases Team will be used for purchases and assignments related to this partner')