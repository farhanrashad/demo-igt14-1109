# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ot_days_diff_payslip_start = fields.Integer(string='Overtime Days Difference before Payslip Start Date', default=0)
    ot_days_diff_payslip_start = fields.Integer(string='Overtime Days Difference after Payslip Start Date', default=0)

