# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from babel.dates import format_date
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.release import version


class PurchaseTeam(models.Model):
    _name = "purchase.team"
    _inherit = ['mail.thread']
    _description = "Purchase Team"
    _order = "sequence"
    _check_company_auto = True
    
    def _get_default_team_id(self, user_id=None, domain=None):
        user_id = user_id or self.env.uid
        user_purchaseteam_id = self.env['res.users'].browse(user_id).purchase_team_id.id
        # Avoid searching on member_ids (+1 query) when we may have the user salesteam already in cache.
        team = self.env['purchase.team'].search([
            ('company_id', 'in', [False, self.env.company.id]),
            '|', ('user_id', '=', user_id), ('id', '=', user_purchaseteam_id),
        ], limit=1)
        if not team and 'default_team_id' in self.env.context:
            team = self.env['purchase.team'].browse(self.env.context.get('default_team_id'))
        return team or self.env['purchase.team'].search(domain or [], limit=1)
    
    
    name = fields.Char('Purchases Team', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean(default=True, help="If the active field is set to false, it will allow you to hide the Purchase Team without removing it.")
    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        related='company_id.currency_id', readonly=True)
    user_id = fields.Many2one('res.users', string='Team Leader', check_company=True)
    # memberships
    member_ids = fields.One2many(
        'res.users', 'purchase_team_id', string='Channel Members',
        check_company=True, domain=[('share', '=', False)],
        help="Add members to automatically assign their documents to this sales team. You can only be member of one team.")
    # UX options
    color = fields.Integer(string='Color Index', help="The color of the channel")
    