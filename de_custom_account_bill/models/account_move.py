# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_bill_id = fields.Many2one('account.custom.bill', 'Custom Bill', ondelete='set null', index=True)
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    custom_bill_line_id = fields.Many2one('account.custom.bill.line', 'Custom Bill Line', ondelete='set null', index=True)
    custom_bill_id = fields.Many2one('account.custom.bill', 'Custom Bill', related='custom_bill_line_id.custom_bill_id', readonly=True)