from odoo import models, fields


class HrContractOvertime(models.Model):
    _inherit = 'hr.contract'

    rate_hour = fields.Monetary('Hour Wage')
    rate_day = fields.Monetary('Day Wage')
