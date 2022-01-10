# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _name = 'hr.employee'

    visa_lines = fields.One2many('hr.visa', 'employee_id')


class EmployeeVisa(models.Model):
    _name = 'hr.visa'
    _description = 'HR Employee Visa'

    @api.onchange('employee_id', 'visa_Type_id')
    def onchange_des(self):
        if self.employee_id and self.visa_Type_id:
            self.description = str(self.visa_Type_id.name) + ' ' + str(self.employee_id.name)
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.visa') 
        values['name'] = seq
        res = super(EmployeeVisa,self).create(values)
        return res
    
    #visa_id = fields.Many2one('hr.employee', string='Visa', index=True, required=True, ondelete='cascade')
    name = fields.Char(string='Visa Reference',  readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    
    description = fields.Char('Description')
    employee_id = fields.Many2one('hr.employee', String="Employee", required=True, readonly=True,states={'draft': [('readonly', False)]},)
    
    visa_Type_id = fields.Many2one('hr.visa.type', String="Visa Type",  required=1, readonly=True,states={'draft': [('readonly', False)]},)
    Visa_issuance_Date = fields.Date(string="Issuance Date", required=1, readonly=True,states={'draft': [('readonly', False)]},)
    Visa_Expiration_Date = fields.Date(string="Expiration Date", required=1, readonly=True,states={'draft': [('readonly', False)]},)
    Visa_country = fields.Many2one('res.country', string="Country", required=1, readonly=True,states={'draft': [('readonly', False)]},)
    no_of_entries = fields.Selection([('single', 'Single Entry Visa'),
                                      ('double', 'Double Entry Visa'),
                                      ('multiple', 'Multiple Entry Visa')], required=True, readonly=True,states={'draft': [('readonly', False)]},)
    state = fields.Selection(
        [('draft', 'To Request'), ('in_process', 'In Process'), ('approve', 'Approve'), ('reject', 'Reject'),
         ('expired', 'Expired')], string='status', default='draft')

    def to_request(self):
        self.state = 'in_process'

    def approve_action(self):
        self.state = 'approve'

    def reject_action(self):
        self.state = 'reject'

    def expired_action(self):
        self.state = 'expired'


class VisaType(models.Model):
    _name = 'hr.visa.type'

    name = fields.Char(String="Visa Type", required=1)
