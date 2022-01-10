# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    custom_entry_eb_history_line = fields.One2many('account.custom.entry.ebh.line', 'custom_entry_id', string='Entry Line for Electricity Bill', copy=True, auto_join=True,)
    
class CustomEntryLine(models.Model):
    _name = 'account.custom.entry.ebh.line'
    _description = 'Custom Entry Line Electricity Bill History'
    
    custom_entry_id = fields.Many2one('account.custom.entry', string='Custom Entry', required=True, ondelete='cascade', index=True, copy=False)
    
    project_id = fields.Many2one('project.project', string="Project", check_company=True, ondelete='cascade')
    amount = fields.Float(string='amount')
    company_id = fields.Many2one('res.company', related='custom_entry_id.company_id')
    currency_id = fields.Many2one('res.currency', related='custom_entry_id.currency_id')


