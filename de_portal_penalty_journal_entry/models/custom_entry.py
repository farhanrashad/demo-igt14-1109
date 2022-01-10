# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CustumEntry(models.Model):
    _inherit = 'account.custom.entry'    
    
    correction_reason = fields.Char(string='Correction Reason', tracking=True)
    allow_correction = fields.Boolean(string='Allow Correction')
    
    def action_correction_entry(self):
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['account.custom.entry'].browse(selected_ids)
        return {
            'name': ('Correction Reason'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'entry.correction.reason',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_custom_entry_id': self.id},
        }
       
class CustumEntryline(models.Model):
    _inherit = 'account.custom.entry.line'
    

class CustumEntrystage(models.Model):
    _inherit = 'account.custom.entry.stage'    

class MailMessage(models.Model):
    _inherit = 'mail.message'    