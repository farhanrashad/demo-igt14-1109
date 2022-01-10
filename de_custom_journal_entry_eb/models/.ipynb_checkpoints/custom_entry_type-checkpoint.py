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
    
    has_electricity = fields.Selection(CATEGORY_SELECTION, string="Has Electricity", default="no", required=True,)
