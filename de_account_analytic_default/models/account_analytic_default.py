# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticDefault(models.Model):
    _inherit = "account.analytic.default"

    employee_id = fields.Many2one('hr.employee', string='Employee', ondelete='cascade', help="Select a Employee")
    department_id = fields.Many2one('hr.department', string='Department', ondelete='cascade', help="Select a Department")
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade', help="Select a Project")

    

    @api.model
    def account_get(self, product_id=None, partner_id=None, account_id=None, user_id=None, project_id=None, department_id=None, employee_id=None, date=None, company_id=None):
        domain = []
        if product_id:
            domain += ['|', ('product_id', '=', product_id)]
        domain += [('product_id', '=', False)]
        if partner_id:
            domain += ['|', ('partner_id', '=', partner_id)]
        domain += [('partner_id', '=', False)]
        if account_id:
            domain += ['|', ('account_id', '=', account_id)]
        domain += [('account_id', '=', False)]
        if company_id:
            domain += ['|', ('company_id', '=', company_id)]
        domain += [('company_id', '=', False)]
        if user_id:
            domain += ['|', ('user_id', '=', user_id)]
        domain += [('user_id', '=', False)]
        if project_id:
            domain += ['|', ('project_id', '=', project_id)]
        domain += [('project_id', '=', False)]
        if department_id:
            domain += ['|', ('department_id', '=', department_id)]
        domain += [('department_id', '=', False)]
        if employee_id:
            domain += ['|', ('employee_id', '=', employee_id)]
        domain += [('employee_id', '=', False)]
        if date:
            domain += ['|', ('date_start', '<=', date), ('date_start', '=', False)]
            domain += ['|', ('date_stop', '>=', date), ('date_stop', '=', False)]
        best_index = -1
        res = self.env['account.analytic.default']
        for rec in self.search(domain):
            index = 0
            if rec.product_id: index += 1
            if rec.partner_id: index += 1
            if rec.account_id: index += 1
            if rec.company_id: index += 1
            if rec.user_id: index += 1
            if rec.project_id: index += 1
            if rec.department_id: index += 1
            if rec.employee_id: index += 1
            if rec.date_start: index += 1
            if rec.date_stop: index += 1
            if index > best_index:
                res = rec
                best_index = index
        return res
