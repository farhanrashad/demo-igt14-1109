# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from random import randint

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    has_spare_penalty = fields.Selection(CATEGORY_SELECTION, string="Has Spare Parts Penalty", default="no", required=True,)
