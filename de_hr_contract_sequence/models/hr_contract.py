# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HRContract(models.Model):
    _inherit = 'hr.contract'
    
    @api.model
    def create(self, vals):
            
        vals['name'] = self.env['ir.sequence'].get('hr.contract') or ' '
        res_id = super(HRContract, self).create(vals)
        return res_id
