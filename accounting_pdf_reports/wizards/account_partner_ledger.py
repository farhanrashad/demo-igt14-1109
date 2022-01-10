# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.common.partner.report"
    _name = "report.partner.ledger"
    _description = "Account Partner Ledger"

    amount_currency = fields.Boolean("With Currency",
                                     help="It adds the currency column on report if the "
                                          "currency differs from the company currency.")
    reconciled = fields.Boolean('Reconciled Entries')
    partner_id = fields.Many2many('res.partner', string='Partners')
    currency_id = fields.Many2one('res.currency', string='Currencies', required=True)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency})
        data = {'form': data['form'], 'partner_id': self.partner_id, 'currency_id': self.currency_id.id,
                'currency_symbol': self.currency_id.symbol}
        return self.env.ref('accounting_pdf_reports.action_report_partnerledger').report_action(self, data=data)
