# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_entry_id = fields.Many2one('account.custom.entry', 'Custom Entry', ondelete='set null', index=True)
    
    