# -*- coding: utf-8 -*-

from dateutil import relativedelta
# from datetime import datetime, timedelta
from datetime import datetime
# import pandas as pd
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.resource.models.resource import HOURS_PER_DAY
import dateutil.parser

READONLY_STATES = {
    'approve1': [('readonly', True)],
    'approve2': [('readonly', True)],
    'approved': [('readonly', True)],
    'Hold': [('readonly', True)],
    'paid': [('readonly', True)],
    'cancel': [('readonly', True)],
    'refused': [('readonly', True)],
}


class HrOvertimeType(models.Model):
    _name = 'hr.overtime.type'
    _description = "HR Overtime Type"

    name = fields.Char('Name', required=True)
    type = fields.Selection([('cash', 'Cash'),
                             ('leave', 'Leave ')], default='cash')
    active = fields.Boolean('Active', default=True)

    duration_type = fields.Selection([('hours', 'Hour'),
                                      ('days', 'Days')],
                                     string='Duration Type', default='hours')
    duration_rule = fields.Selection([('unlimited', 'Unlimited'),
                                      ('fixed', 'Fixed ')], default='unlimited', string='Limit Per Day')
    duration_limit = fields.Float(string='Duration Limit')
    leave_earn_hours = fields.Float(string='Leave Earning Total Hours')
    pay_rule = fields.Selection([('percent', 'Salary (Pecentage)'),
                                 ('fix', 'Fixed Rate'), ],
                                default='percent', string='Pay Based On')

    total_hours = fields.Float(string='Total Hours Limit', required=True)

    leave_type = fields.Many2one('hr.leave.type', string='Leave Type', )
    leave_compute = fields.Many2many('hr.leave.type', compute="_get_leave_type")
    rule_line_ids = fields.One2many('hr.overtime.type.rule', 'type_line_id')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type already exists!"),
    ]

    @api.onchange('duration_type')
    def _get_leave_type(self):
        dur = ''
        ids = []
        if self.duration_type:
            if self.duration_type == 'days':
                dur = 'day'
            else:
                dur = 'hour'
            leave_type = self.env['hr.leave.type'].search([('request_unit', '=', dur)])
            for recd in leave_type:
                ids.append(recd.id)
            self.leave_compute = ids


class HrOverTimeTypeRule(models.Model):
    _name = 'hr.overtime.type.rule'
    _description = "HR Overtime Type Rule"

    type_line_id = fields.Many2one('hr.overtime.type', string='Over Time Type')
    name = fields.Char('Name', required=True)
    from_duration = fields.Float('From', )
    to_duration = fields.Float('To', )
    duration_type = fields.Selection(related='type_line_id.duration_type')
    overtime_rate = fields.Float('Rate')

    @api.constrains('overtime_rate')
    def _check_overtime_rate_percentage(self):
        for rule in self:
            if rule.overtime_rate < 1 or rule.overtime_rate > 100:
                raise UserError(_('Overtime rate percentage can define between 1 to 100'))


class HrOvertimeRequest(models.Model):
    _name = 'hr.overtime.request'
    _description = "HR Overtime"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _order = 'date_request desc'

    def _get_employee_domain(self):
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.user.id)], limit=1)
        domain = [('id', '=', employee.id)]
        if self.env.user.has_group('hr.group_hr_user'):
            domain = []
        return domain

    @api.depends('overtime_line.overtime_hours')
    def _total_hours(self):
        for order in self:
            tot_hours = 0.0
            for line in order.overtime_line:
                tot_hours += line.overtime_hours
            if order.overtime_type_id.total_hours < tot_hours:
                if order.overtime_type_id.type == 'cash':
                    raise ValidationError(_('You Are Not Allow to Enter Total Hours more than ' + str(
                        order.overtime_type_id.total_hours)))
                elif order.overtime_type_id.type == 'leave':
                    if order.overtime_type_id.leave_earn_hours < tot_hours:
                        raise ValidationError(_('You Are Not Allow to Enter Total Hours more than ' + str(
                            order.overtime_type_id.leave_earn_hours)))
                    else:
                        order.update({
                            'total_hours': tot_hours,
                        })
            else:
                order.update({
                    'total_hours': tot_hours,
                })

    total_hours = fields.Float(string='Total Hours', store=True, compute='_total_hours',
                               tracking=True)

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char('Name', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  domain=_get_employee_domain, default=lambda self: self.env.user.employee_id.id,
                                  required=True, states=READONLY_STATES)
    department_id = fields.Many2one('hr.department', string="Department",
                                    related="employee_id.department_id")
    job_id = fields.Many2one('hr.job', string="Job", related="employee_id.job_id")
    manager_id = fields.Many2one('res.users', string="Manager",
                                 related="employee_id.parent_id.user_id", store=True)
    user_id = fields.Many2one('res.users', string='Responsible', index=True, tracking=True,
                              default=lambda self: self.env.user, check_company=True, states=READONLY_STATES)

    is_manager = fields.Boolean(string='Is Manager', compute='_compute_manager', help='Compute Manager for approval',
                                readonly=True, )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES,
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.company.currency_id.id)

    contract_id = fields.Many2one('hr.contract', string="Contract", related="employee_id.contract_id", )
    date_request = fields.Datetime('Request On', required=True, states=READONLY_STATES, index=True, copy=False,
                                   default=fields.Datetime.now, help="Overtime request date")
    date_submit = fields.Datetime('Submission Date', readonly=1, index=True, copy=False)
    date_approve = fields.Datetime('Confirmation Date', readonly=1, index=True, copy=False)
    desc = fields.Text('Description')
    state = fields.Selection([('draft', 'Draft'),
                              ('approve1', 'Manager Approval'),
                              ('approve2', 'HR Approval'),
                              ('approved', 'Approved'),
                              ('paid', 'Paid'),
                              ('hold', 'Hold'),
                              ('cancel', 'Cancelled'),
                              ('refused', 'Refused')], string="State",
                             default="draft")
    cancel_reason = fields.Text('Refuse Reason')
    leave_id = fields.Many2one('hr.leave.allocation', string="Leave ID")

    overtime_type_id = fields.Many2one('hr.overtime.type', required=True, states=READONLY_STATES)
    type = fields.Selection(related='overtime_type_id.type')
    duration_type = fields.Selection(related='overtime_type_id.duration_type')
    pay_rule = fields.Selection(related='overtime_type_id.pay_rule')

    overtime_rate = fields.Monetary(string='Overtime Rate', compute='_compute_overtime_rate', readonly=True)
    overtime_amount = fields.Monetary(string='Overtime Amount', compute='_compute_overtime_amount', readonly=True,
                                      store=True)

    total_leaves = fields.Float(string='Total Leaves', compute='_compute_leaves', readonly=True)

    overtime_line = fields.One2many('hr.overtime.request.line', 'overtime_request_id', string='Overtime Lines',
                                    copy=True, states=READONLY_STATES)

    @api.depends('overtime_line', 'overtime_line.overtime_hours', 'overtime_line.overtime_days')
    def _compute_leaves(self):
        tot = tot_hrs = tot_days = 0.0
        if self.type == 'leave':
            for line in self.overtime_line:
                tot_hrs += line.overtime_hours
                tot_days += line.overtime_days

            if self.overtime_type_id.duration_type == 'hours':
                tot = tot_hrs / self.overtime_type_id.leave_earn_hours
            else:
                tot = tot_days
        self.total_leaves = tot

    @api.depends('overtime_line', 'overtime_line.overtime_hours', 'overtime_line.overtime_days')
    def _compute_overtime_rate(self):
        self.ensure_one()
        rate_hrs = rate_days = tot_hrs = tot_days = 0.0
        tot_rate_hrs = tot_rate_days = 0.0
        rate = 0.0
        if self.type == 'cash':
            for line in self.overtime_line:
                tot_hrs += line.overtime_hours
                tot_days += line.overtime_days

            for rule in self.overtime_type_id.rule_line_ids:
                if rule.from_duration <= tot_hrs and rule.to_duration >= tot_hrs:
                    tot_rate_hrs = rule.overtime_rate * (self.contract_id.wage / 26 / 7.335)
                if rule.from_duration <= tot_days and rule.to_duration >= tot_days:
                    tot_rate_days = rule.overtime_rate * (self.contract_id.wage / 30)

            if self.duration_type == 'days':
                if self.pay_rule == 'fix':
                    rate = self.contract_id.rate_day
                elif self.pay_rule == 'percent':
                    rate = tot_rate_days + 1.22
            elif self.duration_type == 'hours':
                if self.pay_rule == 'fix':
                    rate = self.contract_id.rate_hour + 1.22
                elif self.pay_rule == 'percent':
                    rate = tot_rate_hrs + 1.22
        self.overtime_rate = rate
        # rules = self.env['hr.overtime.type.rule'].search([('type_line_id','=',line.overtime_request_id.overtime_type_id.id),('from_hrs','<=',tot),('to_hrs','>=',tot)],limit=1)
        # for rule in rules:

    @api.depends('overtime_line', 'overtime_line.overtime_hours', 'overtime_line.overtime_days')
    def _compute_overtime_amount(self):
        tot_hrs = tot_days = amount = 0.0
        for ot in self:
            if ot.type == 'cash':
                for line in ot.overtime_line:
                    tot_hrs += line.overtime_hours
                    tot_days += line.overtime_days
                if ot.duration_type == 'days':
                    amount = tot_days * ot.overtime_rate
                elif ot.duration_type == 'hours':
                    amount = tot_hrs * ot.overtime_rate
        self.overtime_amount = amount

    def _compute_manager(self):
        for ot in self:
            if ot.manager_id == self.env.user:
                ot.is_manager = True
            else:
                ot.is_manager = False

    @api.onchange('employee_id')
    def _get_defaults(self):
        for sheet in self:
            if sheet.employee_id:
                sheet.update({
                    'department_id': sheet.employee_id.department_id.id,
                    'job_id': sheet.employee_id.job_id.id,
                    'manager_id': sheet.sudo().employee_id.parent_id.user_id.id,
                    'overtime_type_id': sheet.sudo().employee_id.overtime_type_id.id,
                })

    @api.depends('date_from', 'date_to')
    def _get_days(self):
        for recd in self:
            if recd.date_from and recd.date_to:
                if recd.date_from > recd.date_to:
                    raise ValidationError('Start Date must be less than End Date')
        for sheet in self:
            if sheet.date_from and sheet.date_to:
                start_dt = fields.Datetime.from_string(sheet.date_from)
                finish_dt = fields.Datetime.from_string(sheet.date_to)
                s = finish_dt - start_dt
                difference = relativedelta.relativedelta(finish_dt, start_dt)
                hours = difference.hours
                minutes = difference.minutes
                days_in_mins = s.days * 24 * 60
                hours_in_mins = hours * 60
                days_no = ((days_in_mins + hours_in_mins + minutes) / (24 * 60))

                diff = sheet.date_to - sheet.date_from
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600
                # sheet.update({
                #    'days_no_tmp': hours if sheet.duration_type == 'hours' else days_no,
                # })

    # @api.onchange('overtime_type_id')
    def _get_hour_amount(self):
        if self.overtime_type_id.rule_line_ids and self.duration_type == 'hours':
            for recd in self.overtime_type_id.rule_line_ids:
                if recd.from_hrs < self.days_no_tmp <= recd.to_hrs and self.contract_id:
                    if self.contract_id.rate_hour:
                        cash_amount = self.contract_id.rate_hour * recd.hrs_amount
                        self.cash_hrs_amount = cash_amount
                    else:
                        raise UserError(_("Hour Overtime Needs Hour Wage in Employee Contract."))
        elif self.overtime_type_id.rule_line_ids and self.duration_type == 'days':
            for recd in self.overtime_type_id.rule_line_ids:
                if recd.from_hrs < self.days_no_tmp <= recd.to_hrs and self.contract_id:
                    if self.contract_id.rate_hour:
                        cash_amount = self.contract_id.rate_hour * recd.hrs_amount
                        self.cash_day_amount = cash_amount
                    else:
                        raise UserError(_("Day Overtime Needs Day Wage in Employee Contract."))

    def action_submit(self):
        # notification to employee
        recipient_partners = [(4, self.user_id.partner_id.id)]
        body = "Your OverTime Request Waiting for Approval"
        msg = _(body)
        # if self.current_user:
        #     self.message_post(body=msg, partner_ids=recipient_partners)

        # notification to finance :
        group = self.env.ref('account.group_account_invoice', False)
        recipient_partners = []
        # for recipient in group.users:
        #     recipient_partners.append((4, recipient.partner_id.id))

        body = "You Get New Time in Lieu Request From Employee : " + str(
            self.employee_id.name)
        msg = _(body)
        # self.message_post(body=msg, partner_ids=recipient_partners)
        return self.sudo().write({
            'state': 'approve1',
            'date_submit': fields.Datetime.now(),
        })

    def action_aprove1(self):
        return self.sudo().write({
            'state': 'approve2',
            'date_approve': fields.Datetime.now(),
        })

    def action_approved(self):
        days = 0
        if self.overtime_type_id.type == 'leave':
            # for line in self.overtime_line:
            # if self.duration_type == 'days':
            holiday_vals = {
                'name': 'Overtime',
                'holiday_status_id': self.overtime_type_id.leave_type.id,
                # 'number_of_days': self.total_leaves,
                'number_of_days': 1,
                'notes': self.desc,
                'holiday_type': 'employee',
                'employee_id': self.employee_id.id,
                'state': 'validate',
            }
            holiday = self.env['hr.leave.allocation'].sudo().create(holiday_vals)
            # else:
            # day_hour = self.days_no_tmp / HOURS_PER_DAY
            # holiday_vals = {
            #    'name': 'Overtime',
            #    'holiday_status_id': self.overtime_type_id.leave_type.id,
            #    'number_of_days': self.total_leaves,
            #    'notes': self.desc,
            #    'holiday_type': 'employee',
            #    'employee_id': self.employee_id.id,
            #    'state': 'validate',
            # }
            # holiday = self.env['hr.leave.allocation'].sudo().create(holiday_vals)
            self.leave_id = holiday.id

        # notification to employee :
        recipient_partners = [(4, self.user_id.partner_id.id)]
        body = "Your Time In Lieu Request Has been Approved ..."
        msg = _(body)
        # self.message_post(body=msg, partner_ids=recipient_partners)
        return self.sudo().write({
            'state': 'approved',
            'date_approve': fields.Datetime.now(),
        })

        # return {
        #     'name': _('Leave Adjust'),
        #     'context': {'default_til_id': self.id},
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'leave.adjust',
        #     'view_id': self.env.ref('leave_management.leave_adjust_wizard_view',
        #                             False).id,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'target': 'new',
        # }

    def action_hold(self):
        self.state = 'hold'

    def action_release(self):
        self.state = 'approve1'

    def reject(self):
        self.state = 'refused'
        # return {
        #     'name': _('Refuse Business Trip'),
        #     'context': {'default_overtime_id': self.id},
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'refuse.wzrd',
        #     'view_id': self.env.ref('leave_management.refuse_wzrd_view',
        #                             False).id,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'target': 'new',
        # }

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        for req in self:
            domain = [
                ('date_from', '<=', req.date_to),
                ('date_to', '>=', req.date_from),
                ('employee_id', '=', req.employee_id.id),
                ('id', '!=', req.id),
                ('state', 'not in', ['refused']),
            ]
            nholidays = self.search_count(domain)
            if nholidays:
                raise ValidationError(_(
                    'You can not have 2 Overtime requests that overlaps on same day!'))

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('hr.overtime') or '/'
        values['name'] = seq
        return super(HrOvertimeRequest, self.sudo()).create(values)

    def unlink(self):
        for overtime in self.filtered(
                lambda overtime: overtime.state != 'draft'):
            raise UserError(
                _('You cannot delete TIL request which is not in draft state.'))
        return super(HrOvertimeRequest, self).unlink()

    # @api.onchange('date_from', 'date_to', 'employee_id')
    def _onchange_date(self):
        holiday = False
        if self.contract_id and self.date_from and self.date_to:
            for leaves in self.contract_id.resource_calendar_id.global_leave_ids:
                leave_dates = pd.date_range(leaves.date_from, leaves.date_to).date
                overtime_dates = pd.date_range(self.date_from, self.date_to).date
                for over_time in overtime_dates:
                    for leave_date in leave_dates:
                        if leave_date == over_time:
                            holiday = True
            if holiday:
                self.write({
                    'public_holiday': 'You have Public Holidays in your Overtime request.'})
            else:
                self.write({'public_holiday': ' '})
            hr_attendance = self.env['hr.attendance'].search(
                [('check_in', '>=', self.date_from),
                 ('check_in', '<=', self.date_to),
                 ('employee_id', '=', self.employee_id.id)])
            self.update({
                'attendance_ids': [(6, 0, hr_attendance.ids)]
            })


class HrOvertimeRequestLine(models.Model):
    _name = 'hr.overtime.request.line'
    _description = "HR Overtime Line"

    overtime_request_id = fields.Many2one('hr.overtime.request', string='Overtime Reference', index=True, required=True,
                                          ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', related='overtime_request_id.employee_id')
    type = fields.Selection(related='overtime_request_id.type', store=True, )
    overtime_type_id = fields.Many2one(related='overtime_request_id.overtime_type_id', store=True, )
    date_overtime = fields.Date('Date', index=True, copy=False, help="Overtime To Date.",
                                compute='_compute_date_orvertime', store=True, readonly=False)

    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date to')
    # overtime_days = fields.Float('Hours', compute="_get_days", store=True)

    state = fields.Selection(related='overtime_request_id.state', store=True, )

    overtime_hours = fields.Float('Overtime Hours', compute='_compute_overtime', store=True, )
    overtime_days = fields.Float('Days', default=1)

    currency_id = fields.Many2one(related='overtime_request_id.currency_id', store=True, string='Currency',
                                  readonly=True)

    overtime_amount = fields.Monetary(string='Overtime Amount', compute='_compute_overtime_line_amount', readonly=True)

    approved_amount = fields.Monetary(string='Approved Amount')

    @api.constrains('approved_amount')
    def _check_approved_amount(self):
        for line in self:
            if line.approved_amount > line.overtime_amount:
                raise UserError(_('You can not approve higher amount of calculated overtime'))

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        for req in self:
            domain = [
                ('date_from', '<=', req.date_to),
                ('date_to', '>=', req.date_from),
                ('employee_id', '=', req.employee_id.id),
                ('id', '!=', req.id),
                ('state', 'not in', ['refused']),
            ]
            nholidays = self.search_count(domain)
            if nholidays:
                raise ValidationError(_(
                    'You can not have 2 Overtime requests that overlaps on same day!'))

        # for line in self:
        #   if line.overtime_type_id.duration_limit == 'fixed':
        #      if line.overtime_request_id.duration_type == 'hours':
        #         if line.overtime_hours > line.overtime_type_id.duration_limit:
        #            raise UserError(_('Overtime exceeding the day limit'))
        #   elif line.overtime_request_id.duration_type == 'days':
        #       if line.overtime_days > line.overtime_type_id.duration_limit:
        #         raise UserError(_('Overtime exceeding the day limit'))

    @api.depends('overtime_hours', 'overtime_days')
    def _compute_overtime_line_amount(self):
        for line in self:
            tot = 0.0
            if line.type == 'cash':
                if line.overtime_request_id.duration_type == 'days':
                    tot = line.overtime_days * line.overtime_request_id.overtime_rate
                else:
                    tot = line.overtime_hours * line.overtime_request_id.overtime_rate
                # tot = 1
            line.update({
                'overtime_amount': tot,
            })

    @api.onchange('overtime_amount')
    def _onchange_overtime_amount(self):
        if self.overtime_amount:
            self.approved_amount = self.overtime_amount

    @api.depends('date_from')
    def _compute_date_orvertime(self):
        for request in self:
            if request.date_from:
                date_from = str(request.date_from)
                request.date_overtime = request.date_from.strftime('%Y-%m-%d')

    @api.depends('date_from', 'date_to')
    def _compute_overtime(self):

        for recd in self:

            if recd.date_from and recd.date_to:
                if recd.date_from > recd.date_to:
                    raise ValidationError('Start Date must be less than End Date')
        for sheet in self:
            if sheet.date_from and sheet.date_to:
                start_dt = fields.Datetime.from_string(sheet.date_from)
                finish_dt = fields.Datetime.from_string(sheet.date_to)
                s = finish_dt - start_dt
                difference = relativedelta.relativedelta(finish_dt, start_dt)
                hours = difference.hours
                minutes = difference.minutes
                days_in_mins = s.days * 24 * 60
                hours_in_mins = hours * 60
                days_no = ((days_in_mins + hours_in_mins + minutes) / (24 * 60))

                diff = sheet.date_to - sheet.date_from
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds / 3600
                if sheet.overtime_request_id.overtime_type_id.duration_rule == 'fixed':
                    if hours > sheet.overtime_request_id.overtime_type_id.duration_limit:
                        raise ValidationError('Overtime Hours Should not be greater than ' + str(
                            sheet.overtime_request_id.overtime_type_id.duration_limit))
                    else:
                        sheet.update({
                            'overtime_hours': hours if sheet.overtime_request_id.duration_type == 'hours' else days_no,
                        })
                else:
                    sheet.update({
                        'overtime_hours': hours if sheet.overtime_request_id.duration_type == 'hours' else days_no,
                    })



