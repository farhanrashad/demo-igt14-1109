# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_entry_id = fields.Many2one('account.custom.entry', 'Custom Entry', ondelete='set null', index=True, copy=False)
    
    @api.onchange('custom_entry_id')
    def _onchange_custom_entry_id(self):
        if not self.custom_entry_id:
            return

        # Copy data from Custom Entry
        invoice_vals = self.custom_entry_id.with_company(self.custom_entry_id.company_id)._prepare_invoice()
        #del invoice_vals['ref']
        self.update(invoice_vals)

        # Copy Bill lines.
        custom_entry_lines = self.custom_entry_id.custom_entry_line - self.line_ids.mapped('custom_entry_line_id')
        new_lines = self.env['account.move.line']
        for line in custom_entry_lines:
            new_line = new_lines.new(line._prepare_account_move_line(self))
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line
        new_lines._onchange_mark_recompute_taxes()
    
    def _check_balanced(self):
        ''' Assert the move is fully balanced debit = credit.
        An error is raised if it's not the case.
        '''
        moves = self.filtered(lambda move: move.line_ids)
        if not moves:
            return

        # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
        # are already done. Then, this query MUST NOT depend of computed stored fields (e.g. balance).
        # It happens as the ORM makes the create with the 'no_recompute' statement.
        self.env['account.move.line'].flush(self.env['account.move.line']._fields)
        self.env['account.move'].flush(['journal_id'])
        self._cr.execute('''
            SELECT line.move_id, ROUND(SUM(line.debit - line.credit), currency.decimal_places)
            FROM account_move_line line
            JOIN account_move move ON move.id = line.move_id
            JOIN account_journal journal ON journal.id = move.journal_id
            JOIN res_company company ON company.id = journal.company_id
            JOIN res_currency currency ON currency.id = company.currency_id
            WHERE line.move_id IN %s
            GROUP BY line.move_id, currency.decimal_places
            HAVING ROUND(SUM(line.debit - line.credit), currency.decimal_places) != 0.0;
        ''', [tuple(self.ids)])

        query_res = self._cr.fetchall()
        if query_res:
            ids = [res[0] for res in query_res]
            sums = [res[1] for res in query_res]
            if not self.custom_entry_id:
                raise UserError(_("Cannot create unbalanced journal entry. Ids: %s\nDifferences debit - credit: %s") % (ids, sums))
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    custom_entry_line_id = fields.Many2one('account.custom.entry.line', 'Custom Entry Line', ondelete='set null', index=True, copy=False)
    custom_entry_id = fields.Many2one('account.custom.entry', 'Custom Entry', related='custom_entry_line_id.custom_entry_id', readonly=True)