# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class HrAttendanceExt(models.Model):
    _inherit = 'hr.attendance'

    @api.onchange('check_in', 'check_out')
    def _onchange_check_in(self):
        for rec in self:
            employees = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            for emp in employees:
                if rec.check_in:
                    emp.emp_state = 'present'
                if rec.check_out:
                    emp.emp_state = 'absent'


class HrEmployeeExt(models.Model):
    _inherit = 'hr.employee'

    def action_check_in(self):
        self.write({
            'emp_state': 'present',
        })

    def action_check_out(self):
        self.write({
            'emp_state': 'absent',
        })

    skype_id = fields.Char(string='Skype Id')
    whatsapp = fields.Char(string='Whatsapp ID')
    assign_region = fields.Char(string='Assigned Region')
    desk = fields.Selection([
        ('fixed_desk', 'Fixed Desk'),
        ('shared_desk', 'Shared Desk')], string='Desk',
        default='fixed_desk')
    is_able_to_edit = fields.Boolean(string='Right to edit')
    manager = fields.Boolean(string='Is a Manager')
    level = fields.Selection([
        ('chief', 'Chief'),
        ('director', 'Director'),
        ('sr_manager', 'Sr.Manager'),
        ('manager', 'Manager'),
        ('non_manager', 'Non Manager'),
        ('consultant', 'Consultant')], string='Level',
        default='chief')
    visibility = fields.Selection([
        ('public', 'Public'),
        ('private', 'Private')], string='Visibility',
        default='public')
    ssnid = fields.Char(string='SSN No')
    sinid = fields.Char(string='SIN No')
    nationality = fields.Char(string='Nationality')
    religion = fields.Selection([
        ('buddhist', 'Buddhist'),
        ('christian', 'Christian'),
        ('islam', 'Islam'),
        ('hindu', 'Hindu'),
        ('non_religious', 'Non Religious'),
        ('chinese_traditional', 'Chinese Traditional'),
        ('african_traditional', 'African Traditional'),
        ('sikhism', 'Sikhism'),
        ('spiritism', 'Spiritism'),
        ('judaism', 'Judaism'),
        ('bahai', 'Bahai'),
        ('jainism', 'Jainism'),
        ('shinto', 'Shinto'),
        ('cao_dai', 'Cao Dai'),
        ('zoroastrianism', 'Zoroastrianism'),
        ('tenrikyo', 'Tenrikyo'),
        ('neo_paganism', 'Neo Paganism'),
        ('unitarian_universalism', 'Unitarian Universalism'),
        ('rastafari', 'Rastafari')], string='Religion',
        default='islam')
    passport_id = fields.Char(string='Passport No')
    passport_expiring_date = fields.Date(string='Passport Expiring Date')
    ssb = fields.Char(string='SSB No.')
    tax_book_no = fields.Char(string='Tax Book No')
    visa_number = fields.Char(string='Visa Number')
    visa_expiring_date = fields.Date(string='Visa Expiring Date')
    frc_number = fields.Char(string='FRC Number')
    frc_expiring_date = fields.Date(string='FRC Expiring Date')
    next_visa_trip_date = fields.Date(string='Next Visa Trip Date')
    bank_account_id = fields.Many2one(comodel_name='res.partner.bank', string='Bank Account International')
    bank_account_local_id = fields.Many2one(comodel_name='res.partner.bank', string='Bank Account Local')
    address_home_id = fields.Many2one(comodel_name='res.partner', string='Home Address')
    myanmar_address_obsolete = fields.Char(string='Address in Myanmar[Obsolete]')
    myanmar_address_current = fields.Char(string='Address in Myanmar[Current]')
    myanmar_address = fields.Many2one(comodel_name='res.partner', string='Address in Myanmar')
    contact_name = fields.Char(string='Contact Name')
    contact_email = fields.Char(string='Contact Email')
    contact_phone = fields.Char(string='Contact Phone')
    contact_country = fields.Many2one(comodel_name='res.country', string='Contact Country')
    num_dependents = fields.Integer(string='Number of Dependents')
    employee_age = fields.Integer(string='Age')
    relationship = fields.Char(string='Relationship')
    passport = fields.Char(string='Passport /NRC')
    date_of_birth = fields.Date(string='DOB')
    is_dependant = fields.Boolean(string='Dependant(Non-working) & Unmarried')
    medic_exam = fields.Date(string='Medical Exam')
    vehicle = fields.Char(string='Company Vehicle')
    vehicle_distance = fields.Integer(string='Home-Work Dist')
    evaluation_plan_id = fields.Char(string='Appraisal Plan')
    evaluation_date = fields.Date(string='Next Appraisal Date')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Analytic Journal')
    emp_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent')], string='Attendance',
        default='present')
    induction_pack_received = fields.Boolean(string='Induction Pack Received')
    is_blacklist = fields.Boolean(string='Blacklisted')
    fingerprint_id = fields.Integer(string='Fingerprint ID')
    work_location = fields.Char(string='Office Location')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Cost Center')
    root_department_id = fields.Many2one(comodel_name='hr.department', string='Root Department Team')
    sub_team_id = fields.Many2one(comodel_name='hr.department', string='Sub-team')
    family_name = fields.Char(string='Name')
    emergency_contact_name = fields.Char(string='Contact Name')
    emergency_contact_email = fields.Char(string='Contact Email')
    emergency_contact_phone = fields.Char(string='Contact Phone')
    emergency_contact_country = fields.Many2one(comodel_name='res.country', string='Contact Country')
    b_to_b_sim_no = fields.Char(string='B2B Sim No.')
    pay_grade = fields.Char(string='Pay Grade')
    number_of_dependents_hr = fields.Char(string='Number of Dependents (HR)')
    medical_insurance = fields.Char(string='Medical Insurance')
    medical_insurance_us = fields.Char(string='Medical Insurance (US$)')
    dependent_medical_insurance = fields.Char(string='Dependent Medical Insurance')
    dependent_medical_insurance_us = fields.Char(string='Dependent Medical Insurance (US$)')
    life_insurance = fields.Char(string='Life Insurance')
    life_cover = fields.Char(string='Life Cover')
    personal_accident = fields.Char(string='Personal Accident')
    personal_accident_cover_us = fields.Char(string='Personal Accident Cover (US$)')
    categories = fields.Char(string='Categories')
    housing_allowance = fields.Char(string='Housing Allowance')
    education_allowance = fields.Char(string='Education Allowance')
    notice_period_months = fields.Char(string='Notice Period (Months)')
    contract_based = fields.Char(string='Contract Based')
    assigned_team = fields.Char(string='Assigned Team')
    assigned_category = fields.Char(string='Assigned Category')
    housing_allowance_actual = fields.Char(string='Housing Allowance Actual')
    housing_allowance_period_from = fields.Date(string='Housing Allowance Period From')
    housing_allowance_period_to = fields.Date(string='Housing Allowance Period To')
    post_paid_ph_card_user = fields.Char(string='Post Paid Phone Card User')



