from odoo import api, fields, models,_


class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    employee_family_ids = fields.One2many('hr.employee.family', 'employee_id')


class HrEmployeeFamily(models.Model):

    _name = 'hr.employee.family'
    _description = "Employee Family"

    @api.onchange('contact')
    def change_name(self):
            for rec in self:
                rec.name = self.contact.name
                # rec.visible_field = True

    name = fields.Char(string="Name",required=True)
    contact = fields.Many2one('res.partner')
    mobile = fields.Char(string="Mobile",related="contact.mobile")
    phone = fields.Char(string="Phone",related="contact.phone")
    email = fields.Char(string="Email",related="contact.email")
    relation_ship = fields.Selection([('father','Father'),
                                      ('mother','Mother'),
                                      ('brother','Brother'),
                                      ('sister','Sister'),
                                      ('husband','Husband'),
                                      ('wife','Wife'),
                                      ('child','Child')], string='Relationship',required=True, default='father')

    date_of_birth = fields.Date()
    # visible_field = fields.Boolean(default=False)
    employee_id = fields.Many2one('hr.employee')
    familty_active = fields.Boolean(string='Active', default=True)

