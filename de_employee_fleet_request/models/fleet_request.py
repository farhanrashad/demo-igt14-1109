# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

class FleetRequest(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'fleet.request'
    _description = 'Employee Fleet Request'
    _rec_name = 'seq_name'

    requested_model = fields.Many2one('fleet.vehicle', string='Vehicle')
    requested_brand_id = fields.Many2one('fleet.vehicle.model.brand', 'Brand', related="requested_model.brand_id",
                                       store=True,
                                       readonly=True)
    request_for = fields.Char(string='Request For', required=1)

    def compute_request_to(self):
        member_list = []
        group_members = self.env['res.groups'].search([('category_id.name','=','Fleet Requests')])
        return [('id', 'in', group_members.users.ids)]
         
    request_to = fields.Many2one('res.users', string='Request To', domain=compute_request_to)
    license_plate = fields.Char(related='requested_model.license_plate',readonly=False)
    image_fleet_request = fields.Image(readonly=False)
    request_date = fields.Date(string='Request Date', default=datetime.today())
    number = fields.Char(string='Number', compute='compute_number')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    employee = fields.Many2one('hr.employee', string='Employee', required=1)
    department = fields.Many2one(related='employee.department_id',store=True,)
    created_by = fields.Many2one (string = "Created By",readonly=True, comodel_name = 'res.users', default = lambda self:self.env.user.id)
    line_manager = fields.Many2one(string="Line Manager", related='employee.parent_id')
    is_line_manager = fields.Boolean(string="Manager Check", compute='manager_check')
    project = fields.Many2one('project.project', string='Project')
    task = fields.Many2one('project.task', string='Task')
    notes = fields.Text(string='Notes')
    request_details = fields.Text(string='Request Details')
    confirm_by = fields.Many2one('res.users', string='Confirm By')
    approve_by = fields.Many2one('res.users', string='Approve By')
    assign_by = fields.Many2one('res.users', string='Assign By')
    return_by = fields.Many2one('res.users', string='Return By')
    confirm_date = fields.Date(string='Confirm Date')
    approve_date = fields.Date(string='Approve Date')
    assign_date = fields.Date(string='Assign Date')
    return_date = fields.Date(string='Return Date')
    seq_name = fields.Char('FR Sequence', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
#         ('approved', 'Approved'),
        ('first_approved', '1st Approved'),
        ('second_approved', '2nd Approved'),
        ('assigned', 'Assigned'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
    ], string='Status', copy=False, index=True, default='new')

    @api.model
    def create(self, vals):
        if vals.get('seq_name', ('New')) == ('New'):
            vals['seq_name'] = self.env['ir.sequence'].next_by_code('fleet.request.sequence') or _('New')
        print('Yes Exist')
        result = super(FleetRequest, self).create(vals)
        return result
    
    def manager_check(self):
        if self.env.user == self.line_manager.user_id:
            self.is_line_manager = True
        else:
            self.is_line_manager = False
            

    def compute_number(self):
        for record in self:
            record.number = record.seq_name

    def action_new(self):
        self.write({
            'state': 'new',
        })
        
    def rejected(self):
        self.write({
            'state': 'rejected',
        })

    def action_confirmed(self):
        self.write({
            'state': 'confirmed',
            'confirm_by': self.env.user,
            'confirm_date': datetime.today(),
        })

#     def action_approved(self):
        
#         self.write({
#             'state': 'approved',
#             'approve_by': self.env.user,
#             'approve_date': datetime.today(),
#         })
        
    def lm_approve(self):
        
        self.write({
            'state': 'first_approved',
            'approve_date': datetime.today(),
        })
        
    def admin_approve(self):
        
        self.write({
            'state': 'second_approved',
            'approve_date': datetime.today(),
        })

    def action_returned(self):
        self.write({
            'state': 'returned',
            'return_by': self.env.user,
            'return_date': datetime.today(),
        })
        
    def action_reset(self):
        self.write({
            'state': 'new',
            'confirm_by': None,
            'confirm_date': None,
            'approve_by': None,
            'approve_date': None,
            'assign_by': None,
            'assign_date': None,
            'return_by': None,
            'return_date': None,
        })
        
        

class FleetConstraints(models.Model):
    _inherit = 'fleet.vehicle'
    
    
    
#     _sql_constraints = [('vin_sn_uniq', 'unique (vin_sn)', "Chassis No. Already exists!"),]
    
    _sql_constraints = [('license_plate_uniq', 'unique (license_plate)', "Plate No. Already exists!"),]

    
    @api.model
    def create(self, vals):
        if vals['vin_sn']:
            vin_sn = vals['vin_sn'].strip()    
            sql = """ select vin_sn from fleet_vehicle where vin_sn='""" +str(vin_sn)+"""' """
            self.env.cr.execute(sql)
            exists = self.env.cr.fetchone()
            if exists:
                raise UserError(('The Chassis Number Already Exists'))
            else:
                pass
            rec = super(FleetConstraints, self).create(vals)
            return rec
        else:
            raise UserError(('Please Enter Chassis Number'))