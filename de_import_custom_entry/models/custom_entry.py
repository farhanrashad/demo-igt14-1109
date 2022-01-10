# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class CustomEntry(models.Model):
    _inherit = "account.custom.entry"
    
    

    def action_import_entry_line(self):
        return {
            'name': ('Import Line'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.entry.line.import.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_custom_entry_id': self.id},
        }