# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    deduction_fields = fields.Boolean('Deduction Fields')