# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

class CustomEntryType(models.Model):
    _name = 'account.custom.bill.type'
    _description = 'Custom Bill Type'
    _order = 'id'
    
    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    code = fields.Char(string='code',size=2, required=True)
    description = fields.Char(string='Description')
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)

    adv_journal_id = fields.Many2one('account.journal', string="Provisional Journal", required=True, company_dependent=True, check_company=True,)
    adv_account_id = fields.Many2one('account.account',string="Account Element", required=True)
    act_journal_id = fields.Many2one('account.journal', string="Reversal Journal", required=True, company_dependent=True, check_company=True,)