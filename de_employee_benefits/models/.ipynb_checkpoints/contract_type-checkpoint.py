# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContractType(models.Model):
    _name = 'contract.type'
    _description = 'Contract Type'
    
    name = fields.Char(string='Reference')
    sequence_code = fields.Char(string="Code")
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence', copy=False, check_company=True)
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    
    
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].create({
                'name': _('Sequence') + ' ' + vals['sequence_code'],
                'padding': 5,
                'prefix': vals['sequence_code'],
                'company_id': vals.get('company_id'),
            })
        vals['sequence_id'] = sequence.id

        contract_type = super().create(vals)
        return contract_type
    

    def write(self, vals):
        if 'sequence_code' in vals:
            for contract_type in self:
                sequence_vals = {
                    'name': _('Sequence') + ' ' + vals['sequence_code'],
                    'padding': 5,
                    'prefix': vals['sequence_code'],
                }
                if contract_type.sequence_id:
                    contract_type.sequence_id.write(sequence_vals)
                else:
                    sequence_vals['company_id'] = vals.get('company_id', contract_type.company_id.id)
                    sequence = self.env['ir.sequence'].create(sequence_vals)
                    contract_type.sequence_id = sequence
        if 'company_id' in vals:
            for contract_type in self:
                if contract_type.sequence_id:
                    contract_type.sequence_id.company_id = vals.get('company_id')
        return super().write(vals)

    
   