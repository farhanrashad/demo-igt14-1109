# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportGeneralLedger(models.AbstractModel):
    _name = 'report.accounting_pdf_reports.report_general_ledger'
    _description = 'General Ledger Report'

    def _get_account_move_entry(self, accounts, init_balance, sortby, display_account, currency_id, bc_currency_id, account_name):
        """
        :param:
                accounts: the recordset of accounts
                init_balance: boolean value of initial_balance
                sortby: sorting by date or partner and journal
                display_account: type of account(receivable, payable and both)

        Returns a dictionary of accounts with following key and value {
                'code': account code,
                'name': account name,
                'debit': sum of total debit amount,
                'credit': sum of total credit amount,
                'balance': total balance,
                'amount_currency': sum of amount_currency,
                'move_lines': list of move line
        }
        """
        default_currency = self.env.ref('base.main_company').currency_id
        currency_obj = self.env['res.currency'].search([('id', '=', currency_id)])
        bc_currency_obj = self.env['res.currency'].search([('id', '=', bc_currency_id)])
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare initial sql query and Get the initial move lines
        if init_balance:
            init_tables, init_where_clause, init_where_params = MoveLine.with_context(
                date_from=self.env.context.get('date_from'), date_to=False, initial_bal=True)._query_get()
            init_wheres = [""]
            if init_where_clause.strip():
                init_wheres.append(init_where_clause.strip())
            init_filters = " AND ".join(init_wheres)
            filters = init_filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')
            sql = ("""SELECT 0 AS lid, l.account_id AS account_id, '' AS ldate, to_char(l.date, 'MM-YYYY') AS account_period, '' AS lcode, 0.0 AS amount_currency, '' AS lref, 'Initial Balance' AS lname, COALESCE(SUM(l.debit),0.0) AS debit, COALESCE(SUM(l.credit),0.0) AS credit, COALESCE(SUM(l.debit),0.0) AS bc_debit, COALESCE(SUM(l.credit),0.0) AS bc_credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as balance,
            proj.name as project_name, emp.name as employee_name , mv.name as move_name, c.name AS currency_name,  dept.name as department_name, analytic.name as analytic_account,  
            COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as bc_balance, '' AS lpartner_id,\
                '' AS move_name, '' AS mmove_id, '' AS currency_code,\
                NULL AS currency_id,\
                '' AS invoice_id, '' AS invoice_type, '' AS invoice_number,\
                '' AS partner_name\
                FROM account_move_line l\
                LEFT JOIN account_move m ON (l.move_id=m.id)\
                LEFT JOIN res_currency c ON (l.currency_id=c.id)\
                LEFT JOIN res_partner p ON (l.partner_id=p.id)\
                LEFT JOIN account_move mv ON (l.move_id=mv.id)\
                LEFT JOIN project_project proj ON (l.project_id = proj.id)\
                LEFT JOIN hr_employee emp ON (l.employee_id = emp.id)\
                LEFT JOIN hr_department dept ON (emp.department_id = dept.id)\
                LEFT JOIN account_analytic_account analytic ON (l.analytic_account_id = analytic.id)\
                JOIN account_journal j ON (l.journal_id=j.id)\
                WHERE l.account_id IN %s""" + filters + ' GROUP BY l.account_id, mv.name, l.date, c.name, proj.name, emp.name, dept.name, analytic.name')
            params = (tuple(accounts.ids),) + tuple(init_where_params)
            cr.execute(sql, params)
            for row in cr.dictfetchall():
                move_lines[row.pop('account_id')].append(row)

        sql_sort = 'l.date, l.move_id'
        if sortby == 'sort_journal_partner':
            sql_sort = 'j.code, p.name, l.move_id'

        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = MoveLine._query_get()
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        filters = filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')

        # Get move lines base on sql query and Calculate the total balance of move lines
        sql = ('''SELECT l.id AS lid, l.account_id AS account_id, l.date AS ldate, to_char(l.date, 'MM-YYYY') AS account_period, j.code AS lcode, proj.name as project_name, emp.name as employee_name , analytic.name as analytic_account,
            dept.name as department_name, l.currency_id, l.amount_currency, l.ref AS lref, l.name AS lname, COALESCE(l.debit,0) AS debit, COALESCE(l.credit,0) AS credit, COALESCE(l.debit,0) AS bc_debit, COALESCE(l.credit,0) AS bc_credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS balance, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS bc_balance,\
            m.name AS move_name, c.symbol AS currency_code, acc.name as account_code, c.name AS currency_name, p.name AS partner_name\
            FROM account_move_line l\
            JOIN account_move m ON (l.move_id=m.id)\
            LEFT JOIN res_currency c ON (l.currency_id=c.id)\
            LEFT JOIN res_partner p ON (l.partner_id=p.id)\
            
            LEFT JOIN project_project proj ON (l.project_id = proj.id)\
            LEFT JOIN hr_employee emp ON (l.employee_id = emp.id)\
            LEFT JOIN hr_department dept ON (emp.department_id = dept.id)\
            LEFT JOIN account_analytic_account analytic ON (l.analytic_account_id = analytic.id)\
            JOIN account_journal j ON (l.journal_id=j.id)\
            JOIN account_account acc ON (l.account_id = acc.id) \
            WHERE l.account_id IN %s ''' + filters + ''' GROUP BY l.id, proj.name,  emp.name, dept.name, analytic.name, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.ref, l.name, m.name, acc.name, c.symbol, c.name, p.name ORDER BY ''' + sql_sort)
        params = (tuple(accounts.ids),) + tuple(where_params)
        cr.execute(sql, params)
        count = 0
        for row in cr.dictfetchall():
            count = count + 1
            if default_currency.id != currency_id:
                row['debit'] = round(row['debit'] , 2)
                row['credit'] = round(row['credit'] , 2)
                row['bc_debit'] = round(row['bc_debit'] * bc_currency_obj.rate, 2)
                row['bc_credit'] = round(row['bc_credit'] * bc_currency_obj.rate, 2)
            balance = 0
            bc_balance = 0
            for line in move_lines.get(row['account_id']):
                balance += line['debit'] - line['credit']
                bc_balance += line['debit'] - line['credit']
            #     amount_currency
            row['balance'] += balance
            row['bc_balance'] += bc_balance
            
            if default_currency.id != currency_id:
                row['balance'] = round(row['balance'] * currency_obj.rate, 2)
                row['bc_balance'] = round(row['bc_balance'] * bc_currency_obj.rate, 2)

            move_lines[row.pop('account_id')].append(row)

        # Calculate the debit, credit and balance for Accounts
        account_res = []
        for account in accounts:
            if account_name:
                if  account.id in account_name:
                    currency = account.currency_id and account.currency_id or account.company_id.currency_id
                    res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance', 'bc_balance'])
                    res['code'] = account.code
                    res['name'] = account.name
                    res['move_lines'] = move_lines[account.id]
                    for line in res.get('move_lines'):
                        if default_currency.id != currency_id:
                            line['amount_currency'] = round(line['amount_currency'] , 2)
                        res['debit'] += line['debit']
                        res['credit'] += line['credit']
                        res['balance'] = line['balance']
                        res['bc_balance'] = line['bc_balance']
                    if display_account == 'all':
                        account_res.append(res)
                    if display_account == 'movement' and res.get('move_lines'):
                        account_res.append(res)
                    if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                        account_res.append(res)
            else:
                currency = account.currency_id and account.currency_id or account.company_id.currency_id
                res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance', 'bc_balance'])
                res['code'] = account.code
                res['name'] = account.name
                res['move_lines'] = move_lines[account.id]
                for line in res.get('move_lines'):
                    if default_currency.id != currency_id:
                        line['amount_currency'] = round(line['amount_currency'] , 2)
                    res['debit'] += line['debit']
                    res['credit'] += line['credit']
                    res['balance'] = line['balance']
                    res['bc_balance'] = line['bc_balance']
                if display_account == 'all':
                    account_res.append(res)
                if display_account == 'movement' and res.get('move_lines'):
                    account_res.append(res)
                if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                    account_res.append(res)
                
        return account_res

    @api.model
    def _get_report_values(self, docids, data):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))
        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        display_account = data['form']['display_account']
        codes = []
        account_codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in
                     self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]
#         if data['form'].get('account_id', False):
#         account_codes = [account.name for account in
#                      self.env['account.account'].search([('id', 'in', docs.account_id)])]    

        accounts = docs if model == 'account.account' else self.env['account.account'].search([])
        account_id = docs.account_id.ids
        currency_id = int(data['currency_id'])
        bc_company_id = self.env.company.id
        company = self.env['res.company'].search([('id', '=', bc_company_id)])
        bc_currency_id = company.currency_id.id
        accounts_res = self.with_context(data['form'].get('used_context', {}))._get_account_move_entry(accounts,
                                                                                                       init_balance,
                                                                                                       sortby,
                                                                                                       display_account,
                                                                                                       currency_id,
                                                                                                       bc_currency_id,
                                                                                                      account_id
                                                                                                      )
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
            'account_codes': account_id,
        }
