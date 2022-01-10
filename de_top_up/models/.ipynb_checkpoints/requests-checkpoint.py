from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class TopUpRequest(models.Model):
    _name = 'topup.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Top Up Request model'


    def unlink(self):
        for r in self:
            if r.state == 'approved' or r.state == 'cancelled' or r.state == 'distributed':
                raise UserError(
                    "TOPUP_Request records which are set to Approved/Cancelled/Distributed can't be deleted!")
        return super(TopUpRequest, self).unlink()

    @api.model
    def create(self, values):
        if values.get('topup_req', _('New')) == _('New'):
            values['topup_req'] = self.env['ir.sequence'].next_by_code('topup.request.topup_req') or _('New')
        return super(TopUpRequest, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    topup_req = fields.Char(string='Topup Request', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('waiting for approval', 'Waiting For LM Approval'),
        ('approved', 'Approved'),
        ('approved_hr', 'Waiting for HR Approval'),
        ('approved_admin', 'Waiting for Admin Approval'),
        ('cancelled', 'Cancelled'),
        ('refused', 'Refused'),
        ('distributed', 'Distributed')
    ], string='State', index=True, copy=False, default='draft')

    topup_request_lines = fields.One2many('topup.request.line', 'request_id', string='Request Lines')
    topup_request_lines_category = fields.One2many('topup.request.category.line', 'request_id', string='Request Lines Category')

    # @api.constrains('participants_ids')
    # def constraints_on_selection(self):
    #     if not self.participants_ids:
    #         raise UserError("Please select atleast 1 Employee!")

    def action_submitted(self):
        # flag = 0
        # for rec in self.participants_ids:
        #     flag = 1
        # if flag == 0:
        #     raise UserError("No participants added!")
        # else:
        self.state = 'waiting for approval'

    def action_approved(self):
        if self.is_level == True:
            self.state = 'approved'
        elif self.additional_req == True:
            self.state = 'approved_hr'
        else:
            self.state = 'approved_admin'
        
    def action_approved_hr(self):
        self.state = 'approved_admin'
        
    def action_approved_admin(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancelled'
        
    def action_refuse(self):
        self.state = 'draft'

    def action_distributed(self):
        self.state = 'distributed'
        balance = self.env['topup.balance'].search([('curr_period','=',self.period),('state','=', 'confirmed')], limit=1)
        telenor = 0
        oredoo = 0
        mpt = 0
        mytel = 0
        for request_line in  self.topup_request_lines:
            telenor += request_line.telenor
            oredoo += request_line.ooredoo
            mpt += request_line.mpt  
            mytel += request_line.mytel
            
        for balance_line in balance.topup_balance_lines:
            if  balance_line.operator == 'telenor':       
                balance_line.update({
                    'distributed_qty': balance_line.distributed_qty + telenor
                })
            if  balance_line.operator == 'ooredoo':       
                balance_line.update({
                    'distributed_qty': balance_line.distributed_qty + oredoo
                })
            if  balance_line.operator == 'mpt':       
                balance_line.update({
                    'distributed_qty': balance_line.distributed_qty + mpt
                })
            if  balance_line.operator == 'mytel':       
                balance_line.update({
                    'distributed_qty': balance_line.distributed_qty + mytel
                })    

    current_date = date.today()
    end_date = current_date + timedelta(days=30)

    description = fields.Text(string="Description")
    period = fields.Char(string='Period', compute='_compute_account_period')
    
    requester = fields.Many2one('res.users', default=lambda self: self.env.user, string="Requester", readonly=True)
    manager = fields.Many2one('hr.employee', string="Line Manager", related='requester.employee_id.parent_id')
    department = fields.Many2one('hr.department', string="Department", related='requester.employee_id.department_id')
    representative_batch = fields.Selection(
        [('c-level', 'C-Level'), ('admin & fleet', 'Admin & Fleet'), ('documentation', 'Documentation'),
         ('engineering', 'Engineering'), ('accounting and finance', 'Accounting and Finance'),
         ('government relations and stakeholder engagement', 'Government Relations and Stakeholder Engagement'),
         ('human resources', 'Human Resources'), ('hse', 'HSE'), ('qa', 'QA'),
         ('information & technology', 'Information & Technology'), ('legal', 'Legal'),
         ('noc', 'NOC'),
         ('fields operations (north)', 'Fields Operations (North)'),
         ('fields operations (south)', 'Fields Operations (South)'), ('power', 'Power'),
         ('o&m rms', 'O&M RMS'), ('o&m support', 'O&M Support'), ('project management', 'Project Management'),
         ('rollout & colocation', 'Rollout & Colocation'), ('procurement', 'Procurement'),
         ('supply chain', 'Supply Chain')],
        string="Representative Batch", default='c-level')
    date = fields.Date(string="Date", default=fields.date.today())
    type = fields.Selection([('employee benfit', 'Employee Benefit'), ('category use', 'Category Use')],
                            string="Type", default='employee benfit')
    is_level = fields.Boolean(string='Is C-Level?')
    additional_req = fields.Boolean(string="Additional Request?")
    
    @api.depends('date')
    def _compute_account_period(self):
        for record in self:
            record.period = record.date.strftime("%B-%Y")
            
    @api.onchange('date')
    def onchange_date(self):        
        employees = self.env['hr.employee'].search([('active_emp','=', True)])
        for employee in employees:
            employee.update({
                'active_emp': False
            })        
    
    
    @api.onchange('additional_req')
    def empty_cards_number(self):
        for line in self.topup_request_lines:
            line.update({
                'telenor': False,
                'mytel':False,
                'mpt': False,
                'ooredoo': False,
            })


class EmployeeRequestLine(models.Model):
    _name = 'topup.request.line'
    _description = 'Top Up Request model'

    request_id = fields.Many2one('topup.request', string='Topup Request')

    employee = fields.Many2one('hr.employee', string="Employee", domain="[('active_emp','=', False)]")
    department = fields.Many2one('hr.department', string="Department", related="employee.department_id")
    telenor = fields.Integer(string="Telenor")
    ooredoo = fields.Integer(string="Ooredoo")
    mpt = fields.Integer(string="MPT")
    mytel = fields.Integer(string="MYTEL")
    total = fields.Integer(string="Total", compute="_compute_total")
    remarks = fields.Char(string="Remarks")
    
    
    @api.onchange('employee')
    def onchange_employee(self):        
        for line  in self:
            line.employee.update({
                'active_emp': True
            })
    

    @api.onchange('total')
    def total_const(self):
        for line in self:
            if self.request_id.additional_req:
                if line.total > 2:
                    raise UserError("Total Sum cannot be greater than 2")
            elif self.request_id.is_level:
                if line.total < 0:
                    raise UserError("Total cannot be Less than 0")
            else:
                if line.total > 3:
                    raise UserError("Total cannot be greater than 3")
                    
                    
    
    @api.depends('telenor','ooredoo','mpt','mytel')
    def _compute_total(self):
        for line in self:
            total_cards = line.telenor + line.ooredoo + line.mpt + line.mytel
            line.update({
                'total': total_cards
            })
            
            
class EmployeeRequestLineCategory(models.Model):
    _name = 'topup.request.category.line'
    _description = 'Top Up Request model for Category'

    request_id = fields.Many2one('topup.request', string='Request')

    category = fields.Selection([('BOD', 'BOD'),
                                 ('media', 'Media ( Facebook, Twitter, LinkedIn )'),
                                 ('gps', 'GPS'),
                                 ('hr', 'HR Phone'),
                                 ('it', 'IT server room Alarm system'),
                                 ('cctv', 'CCTV')
                                ], string="Category", default='BOD')
    description = fields.Char(string="Description")
    telenor = fields.Integer(string="Telenor")
    ooredoo = fields.Integer(string="Ooredoo")
    mpt = fields.Integer(string="MPT")
    mytel = fields.Integer(string="MYTEL")
    total = fields.Integer(string="Total", compute="_compute_total")
    remarks = fields.Char(string="Remarks")

                    
    
    @api.depends('telenor','ooredoo','mpt','mytel')
    def _compute_total(self):
        for line in self:
            total_cards = line.telenor + line.ooredoo + line.mpt + line.mytel
            line.update({
                'total': total_cards
            })

    