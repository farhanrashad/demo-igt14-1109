# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    
    has_hse_fields = fields.Selection(CATEGORY_SELECTION, string="HSE Penalties", default="no", required=True,)
    has_pm_fields = fields.Selection(CATEGORY_SELECTION, string="PM Penalties", default="no", required=True,)
    has_sla_fields = fields.Selection(CATEGORY_SELECTION, string="SLA Penalties", default="no", required=True,)
    has_spmrf_fields = fields.Selection(CATEGORY_SELECTION, string="Spare Parts Penalties", default="no", required=True,)
    
    allow_penalty_adjustment = fields.Boolean(string="Allow Penalty Adjustment")
    
class AccountCustomEntryStage(models.Model):
    _inherit = 'account.custom.entry.stage'
    
    allow_penalty_adjustment = fields.Boolean(string="Allow Penalty Adjustment")