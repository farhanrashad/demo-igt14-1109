# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning

   
class JobPositionRequest(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name = 'hr.job.position.request'
    _description = 'Job Position Request'
    
    def job_position_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'hr.job',
            'view_mode': 'tree,form',
            'domain': [('name', '=', self.name)],
        }

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('verify', 'HOD Approval'),
        ('co_approve', 'HR Manager'),
        ('done', 'Done'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    stages = fields.Selection([
        ('new', 'New'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('position_created', 'Job Position Created'),
        ('rejected', 'Rejected')
    ], default='new')
    
    def _get_default_stage_id(self):
        return self.env['job.position.stages'].search([('name', '=', 'New')], limit=1).id
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['job.position.stages'].search([])
        return stage_ids

    stage_id = fields.Many2one('job.position.stages', string='Stage', tracking=True, index=True,
                               default=_get_default_stage_id)

    def unlink(self):
        for leave in self:
            if leave.state in ('done', 'verify', 'co_approve'):
                raise UserError(_('You cannot delete an order form  which is not draft or cancelled. '))
            return super(JobPositionRequest, self).unlink()

    def draft(self):
        self.write({'state': 'submit'})

    def get_manager(self):
        employees = self.env['hr.employee'].search([('user_id', '=', self.env.user)])
        return employees

    def action_submit(self):
        self.write({'stages': 'to_approve'})
        template_id = self.env.ref('openhcm_job_request.new_job_request_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def get_mail_url(self):
        self.ensure_one()
        print('musadiq')
        form_id = self.id
        url = 'http://localhost:8094/web#action=190&model=hr.job.position.request&view_type=list&cids=&menu_id=123'
        return url

    def get_job_position_url(self):
        self.ensure_one()
        url = 'http://localhost:8094/web#action=173&model=hr.job&view_type=kanban&cids=&menu_id=123'
        return url

    def action_approve(self):
        self.write({'stages': 'approved'})
        template_id = self.env.ref('openhcm_job_request.job_position_approve').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def action_create_position(self):
        self.write({'stages': 'position_created'})
        self.env['hr.job'].create({
            'name': self.name,
            'department_id': self.department.id,
            'no_of_recruitment': self.no_of_person_request,
            'user_id': self.requested_by.id
        })
        template_id = self.env.ref('openhcm_job_request.job_position_creation').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def action_reject(self):
        self.write({'stages': 'rejected'})
        template_id = self.env.ref('openhcm_job_request.job_position_rejection').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        
    def submit(self):
        self.write({'state': 'verify'})
        
    def verify(self):
        self.write({'state': 'co_approve'})
        
    def co_approve(self):
        self.env['hr.job'].create({'name': self.name,
                                   'department_id': self.department.id,
                                   'no_of_recruitment': self.no_of_person_request,
                                   'user_id': self.requested_by.id
                                   })
        self.write({'state': 'done'})

    # def default_manager_id(self):
    #     user = self.env.user
    #     emp = self.env['hr.employee'].search([('user_id', '=', self.requested_by.id)])
    #     print('emp', emp)
    #     self.manager_id = emp.parent_id.id

    date = fields.Date(string='Request On', default=datetime.today())
    no_of_person_request = fields.Integer(string='Expected new employee', default='1')
    budget = fields.Boolean(string='Budgeted')
    department = fields.Many2one('hr.department', string='Department', required=True)
    requested_by = fields.Many2one('res.users', string='Requested By',
                                   default=lambda self: self.env.user, readonly=True)
    reason = fields.Text(string='Reason')
    age_preference = fields.Integer(string='Age Preference', default='0')
    get_id = fields.Char(string='Order', readonly=True, copy=False,)
    name = fields.Char(string='Name', required=True)
    qualification = fields.Html(string='Qualifications / Background / Skills Set')
    education = fields.Html(string='Education / Degree Required')
    job_request = fields.Html(string='Job Request / Job Request Required')
    software = fields.Html(string='Software Proficiency Requirements')
    communication = fields.Html(string='Communications')
    preferences_ids = fields.One2many('hr.preferences', 'position_id')
    email_id = fields.Char(string='Email')
    manager_id = fields.Many2one('hr.employee', string='Manager', related='department.manager_id')

    @api.model
    def create(self, vals):
        if 'get_id' not in vals or vals['get_id'] == False:
            sequence = self.env.ref('openhcm_job_request.get_id')
            vals['get_id'] = sequence.next_by_id()
        return super(JobPositionRequest, self).create(vals)
    
    
class HrTeam(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name = 'hr.team'
    _description = 'Hr Team'

    name = fields.Char(string='Name', required=True)


class Preferences(models.Model):
    _name = 'hr.preferences'
    _description = 'Hr Preferences'

    pref_name = fields.Char(string='Name', required=True)
    pref_value = fields.Char(string='Value', required=True)
    position_id = fields.Many2one('hr.job.position.request', string='Position')


class JobPositionStages(models.Model):
    _name = 'job.position.stages'
    _description = 'Position Stage'

    def _get_default_project_ids(self):
        default_project_id = self.env.context.get('default_project_id')
        return [default_project_id] if default_project_id else None

    name = fields.Char(string='Stage Name', required=True, translate=True)
    is_quality = fields.Boolean(string='Active')