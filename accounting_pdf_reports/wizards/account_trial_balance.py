# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report'
    _description = 'Trial Balance Report'

    currency_id = fields.Many2one('res.currency', 'Currency')
    journal_ids = fields.Many2many('account.journal', 'account_balance_report_journal_rel', 'account_id', 'journal_id',
                                   string='Journals', required=True, default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data.update({'currency_id': self.currency_id.id, 'currency_symbol': self.currency_id.symbol})
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('accounting_pdf_reports.action_report_trial_balance').report_action(records, data=data)
