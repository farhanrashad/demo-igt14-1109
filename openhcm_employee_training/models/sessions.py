# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EmployeeTrainingSessions(models.Model):
    _name = 'hr.employee.training.session'
    _description = 'HR Employee Training Sessions'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'


    def action_session_send(self):
        ctx = {}
        email_list = []

        emails = self.participants_lines
        if emails:
            for email in emails:
                email_list.append(email)


        if email_list:
            ctx['email_to'] = ','.join([email.employee_id.email for email in email_list if email])
            ctx['email_from'] = self.env.user.email
            ctx['ref'] = self.name
            ctx['lang'] = self.env.user.lang
            ctx['date_from'] = self.end_date
            ctx['date_to'] = self.start_date
            ctx['location'] = self.delivery_location
            template = self.env.ref('openhcm_employee_training.email_template_edi_sessions_case')
            db = self.env.cr.dbname

            template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)

        self.write({
            'state': 'scheduled',
        })

    def action_process(self):
        self.write({
            'state': 'approval',
        })

    def action_close(self):
        self.write({
            'state': 'cancelled',
        })

    def action_completed(self):
        self.write({
            'state': 'completed',
        })

    def action_schedule(self):
        self.write({
            'state': 'scheduled',
        })

    def action_pending(self):
        self.write({
            'state': 'pending',
        })


    name = fields.Char(string='Order Reference',  copy=False,  index=True, states={'draft': [('readonly', True)]},default=lambda self: _('New'))
    delivery_method = fields.Many2one('hr.employee.training.course.delivery.method', required=True,string='Delivery Method', store=True, states={'draft': [('readonly', False)]},)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    delivery_location = fields.Char(string='Delivery Location', store=True)
    note = fields.Html()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approval', 'Approval'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    trainer_lines = fields.One2many('hr.employee.training.session.trainers', 'session_id', string='Trainer Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True, auto_join=True)
    participants_lines = fields.One2many('hr.employee.training.session.participants', 'session_id', string='Participants Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True, auto_join=True)



    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.training.session')
        values['name'] = seq
        res = super(EmployeeTrainingSessions,self).create(values)
        return res



class TrainingCourseTrainers(models.Model):
    _name = 'hr.employee.training.session.trainers'
    _description = 'HR Employee Training Sessions Trainers'

    session_id = fields.Many2one('hr.employee.training.session',string='Sessions', store=True)
    trainer_id = fields.Many2one('res.partner',string='Trainer', store=True)


class TrainingCourseParticipants(models.Model):
    _name = 'hr.employee.training.session.participants'
    _description = 'HR Employee Training Course Participants'


    session_id = fields.Many2one('hr.employee.training.session',string='Sessions', store=True)
    employee_id = fields.Many2one('res.partner',string='Participants', store=True)  