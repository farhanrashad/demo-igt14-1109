# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    contract_type_id = fields.Many2one('contract.type', string='Contract Type', index=True, ondelete="cascade")
    code = fields.Char(related='contract_type_id.sequence_code')
    sequence_code = fields.Char(string="Sequence Code")
    
    @api.onchange('contract_type_id')
    def _check_code(self):
        self.sequence_code = self.code   
        
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence', copy=False, check_company=True)
    
    
    
    @api.model
    def create(self, vals):            
        vals['name'] = (
        vals.get('code') or
        self.env.context.get('default_code') or
        self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('hr.contract') or
         'New'
        )
        sequence = self.env['ir.sequence'].search([('prefix','=', vals['sequence_code'])
        ], limit=1)
        vals['sequence_id'] = sequence.id
        vals['name'] = sequence.next_by_id()
        contract = super(HrContract, self).create(vals)
        
        
        return contract

    
    
   