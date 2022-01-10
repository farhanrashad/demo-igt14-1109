# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    purchase_team_id = fields.Many2one(
        'purchase.team', "User's Purchase Team",
        help='Purchase Team the user is member of. Used to compute the members of a Purchase Team through the inverse one2many')