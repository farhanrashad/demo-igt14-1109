# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def _get_default_team(self):
        return self.env['purchase.team']._get_default_team_id()

    purchase_user_id = fields.Many2one('res.users', copy=False, tracking=True,
                                       string='Purchase Representative',default=lambda self: self.env.user)
        
    purchase_team_id = fields.Many2one('purchase.team', 'Purchases Team',
        change_default=True, default=_get_default_team,)
