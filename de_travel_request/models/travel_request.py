from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class TravelRequest(models.Model):
    _name = 'travel.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    def unlink(self):
        for r in self:
            if r.state == 'refuse' or r.state == 'approved':
                raise UserError(
                    "Travel Request records which are set to Refuse/Approved can't be deleted!")
        return super(TravelRequest, self).unlink()

    @api.model
    def create(self, values):
        if values.get('travel_request', _('New')) == _('New'):
            values['travel_request'] = self.env['ir.sequence'].next_by_code('travel.request.travel_request') or _('New')
        return super(TravelRequest, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    travel_request = fields.Char('Name', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('refuse', 'Refuse'),
        ('approved', 'Approved'),
    ], string='State', index=True, readonly=True, tracking=True, copy=False, default='draft')

    def action_submit(self):
        self.state = 'submitted'

    def action_refuse(self):
        self.state = 'refuse'

    def action_approve(self):
        self.state = 'approved'
        year_balance = self.env['travel.balance'].search([('crnt_year', '=', datetime.now().year)], limit=1)
        if year_balance:
            for line in year_balance.balance_line_ids:
                if line.employee_id.id == self.employee_id.id:
                    if self.round_trip == True:
                        line.update({
                            'used_balance':   line.used_balance + 1,
                            })
                    elif self.one_way_trip == True:
                        line.update({
                            'used_balance':   line.used_balance + 0.5,
                            })    
                    allocated_balance = line.allocated_balance 
                    remaining_balance = allocated_balance - line.used_balance
                    line.update({
                        'remaining_balance':   remaining_balance,
                        })
                        
        

    def action_set_to_draft(self):
        self.state = 'draft'

    travel_request_lines = fields.One2many('travel.request.line', 'travel_request_id')

    name = fields.Char('Name', required=True, tracking=True)
    description_main = fields.Char('Description')
    travel_type = fields.Selection(
        [('business', 'Business'), ('personal', 'Personal'), ('visa run', 'Visa Run'), ('meeting', 'Meeting')],
        string="Travel Type", default=None)
    ticket_arr_paid = fields.Boolean('Ticket Arranged and Paid by IGT')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    days = fields.Integer(string='Days', compute='get_days')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    designation_id = fields.Many2one('hr.job', string='Designation', related='employee_id.job_id')
    nrc_other_id = fields.Char(string="NRC/Other ID", related="employee_id.identification_id")
    passport_no = fields.Char(string="Passport No", related="employee_id.passport_id")
    dob = fields.Date(string="Date of Birth", related="employee_id.birthday")

    # , default=lambda self: self.env.user  options="{&quot;end_date&quot;: &quot;date_end&quot;}" options="{&quot;start_date&quot;: &quot;date_start&quot;}"  widget="daterange"
    #

    def get_days(self):
        for travel in self:
            if travel.date_start and travel.date_end:
                delta = travel.date_start - travel.date_end
                travel.days = abs(delta.days)
            else:
                travel.days = 0

    # page fields
    visa_exp_date = fields.Date(string="Visa Expiry Date")
    multi_visit_visa = fields.Boolean(string="Multiple Visit Visa")
    round_trip = fields.Boolean(string="Round Trip")
    one_way_trip = fields.Boolean(string="One Way Trip")
    dest_country = fields.Many2one('res.country', string="Destination Country")
    dest_city = fields.Char(string="Destination City")
    ticket_price = fields.Integer(string="Ticket Price")
    visa_cost = fields.Integer(string="Visa Cost")
    description = fields.Text(string="Description")


#     def get_user(self):
#         self.employee_id = self.env.user.name

class TravelRequestLine(models.Model):
    _name = 'travel.request.line'

    travel_request_id = fields.Many2one('travel.request')
    hotel_detail = fields.Char(string="Hotel Detail")
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
