import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_hr_employee_details_report.hr_employee_report_xlsx'
    _description = 'Employee Details Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Employee Details Report')
        sheet.write(3, 0, 'Employee Number', format1)
        sheet.write(3, 1, 'Cost Center', format1)
        sheet.write(3, 2, 'Is Manager', format1)
        sheet.write(3, 3, 'Level', format1)
        sheet.write(3, 4, 'Whatsapp', format1)
        sheet.write(3, 5, 'B2B SIM No.', format1)
        sheet.write(3, 6, 'Assign Region', format1)
        sheet.write(3, 7, 'Pay Grade', format1)
        sheet.write(3, 8, 'Bank Account Local', format1)
        sheet.write(3, 9, 'SIN No.', format1)
        sheet.write(3, 10, 'SSB No.', format1)
        sheet.write(3, 11, 'Tax Book No.', format1)
        sheet.write(3, 12, 'Religion', format1)
        sheet.write(3, 13, 'Passport Expiring Date', format1)
        sheet.write(3, 14, 'FRC Number', format1)
        sheet.write(3, 15, 'FRC Expiring Date', format1)
        sheet.write(3, 16, 'Number of Dependents(HR)', format1)
        sheet.write(3, 17, 'Number of Children', format1)
        sheet.write(3, 18, 'Medical Insurance', format1)
        sheet.write(3, 19, 'Medical Insurance (US$)', format1)
        sheet.write(3, 20, 'Dependent Medical Insurance', format1)
        sheet.write(3, 21, 'Dependent Medical Insurance (US$)', format1)
        sheet.write(3, 22, 'Life Insurance', format1)
        sheet.write(3, 23, 'Life Cover (US$)', format1)
        sheet.write(3, 24, 'Personal Accident', format1)
        sheet.write(3, 25, 'Personal Accident Cover (US$)', format1)
        sheet.write(3, 26, 'Number of Dependents', format1)
        sheet.write(3, 27, 'Categories', format1)
        sheet.write(3, 28, 'Housing Allowance', format1)
        sheet.write(3, 29, 'Education Allowance', format1)
        sheet.write(3, 30, 'Active', format1)
        sheet.write(3, 31, 'Induction Pack Received', format1)
        sheet.write(3, 32, 'Fingerprint ID', format1)
        sheet.write(3, 33, 'Address in Myanmar[Obsolete]', format1)
        sheet.write(3, 34, 'Address in Myanmar[Current]', format1)
        sheet.write(3, 35, 'Notice Period(Month(s))', format1)
        sheet.write(3, 36, 'Contract Based', format1)
        sheet.write(3, 37, 'Assigned Team', format1)
        sheet.write(3, 38, 'Assigned Category', format1)
        sheet.write(3, 39, 'Housing Allowance Actual', format1)
        sheet.write(3, 40, 'Housing Allowance Period From', format1)
        sheet.write(3, 41, 'Housing Allowance Period To', format1)
        sheet.write(3, 42, 'Post Paid Ph Card User', format1)
        

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
        sheet.set_column(row, 4, 20)
        sheet.set_column(row, 5, 20)
        sheet.set_column(row, 6, 20)
        sheet.set_column(row, 7, 20)
        sheet.set_column(row, 8, 20)
        sheet.set_column(row, 9, 20)
        sheet.set_column(row, 10, 20)
        sheet.set_column(row, 11, 20)
        sheet.set_column(row, 12, 20)
        sheet.set_column(row, 13, 20)
        sheet.set_column(row, 14, 20)
        sheet.set_column(row, 15, 20)
        sheet.set_column(row, 16, 20)
        sheet.set_column(row, 17, 20)
        sheet.set_column(row, 18, 20)
        sheet.set_column(row, 19, 20)
        sheet.set_column(row, 20, 20)
        sheet.set_column(row, 21, 20)
        sheet.set_column(row, 22, 20)
        sheet.set_column(row, 23, 20)
        sheet.set_column(row, 24, 20)
        sheet.set_column(row, 25, 20)
        sheet.set_column(row, 26, 20)
        sheet.set_column(row, 27, 20)
        sheet.set_column(row, 28, 20)
        sheet.set_column(row, 29, 20)
        sheet.set_column(row, 30, 20)
        sheet.set_column(row, 31, 20)
        sheet.set_column(row, 32, 20)
        sheet.set_column(row, 33, 20)
        sheet.set_column(row, 34, 20)
        sheet.set_column(row, 35, 20)
        sheet.set_column(row, 36, 20)
        sheet.set_column(row, 37, 20)
        sheet.set_column(row, 38, 20)
        sheet.set_column(row, 39, 20)
        sheet.set_column(row, 40, 20)
        sheet.set_column(row, 41, 20)
        sheet.set_column(row, 42, 20)
        
        for id in lines:
            if id.phone:
                employee_number = id.phone
            else:
                employee_number = None
            try:
                if id.analytic_account_id:
                    cost_center = id.analytic_account_id.name
                else:
                    cost_center = None
            except:
                cost_center = None
            try:
                if id.manager:
                    is_manager = id.manager
                else:
                    is_manager = None
            except:
                is_manager = None
            try:
                if id.level:
                    level = id.level
                else:
                    level = None
            except:
                level = None
            try:   
                if id.whatsapp:
                    whatsapp = id.whatsapp
                else:
                    whatsapp = None
            except:
                whatsapp = None
            try:   
                if id.assign_region:
                    assign_region = id.assign_region
                else:
                    assign_region = None
            except:
                assign_region = None
            try:
                if id.bank_account_local_id:
                    bank_account_local = id.bank_account_local_id.acc_number
                else:
                    bank_account_local = None
            except:
                bank_account_local = None
            if id.sinid:
                sin_id = id.sinid
            else:
                sin_id = None
            if id.ssb:
                ssb_no = id.ssb
            else:
                ssb_no = None
            if id.tax_book_no:
                tax_book_no = id.tax_book_no
            else:
                tax_book_no = None
            if id.religion:
                religion = id.religion
            else:
                religion = None
            if id.passport_expiring_date:
                passport_expiring_date = id.passport_expiring_date
                passport_expiring_date = passport_expiring_date.strftime("%Y%m%d")
            else:
                passport_expiring_date = None
            if id.frc_number:
                frc_number = id.frc_number
            else:
                frc_number = None
            if id.frc_expiring_date:
                frc_expiring_date = id.frc_expiring_date
                frc_expiring_date = frc_expiring_date.strftime("%Y%m%d")
            else:
                frc_expiring_date = None
            if id.children:
                number_of_children = id.children
            else:
                number_of_children = None
            if id.num_dependents:
                num_of_dependents = id.num_dependents
            else:
                num_of_dependents = None
            if id.active:
                active = id.active
            else:
                active = None
            if id.induction_pack_received:
                induction_pack_received = id.induction_pack_received
            else:
                induction_pack_received = None
            if id.fingerprint_id:
                fingerprint_id = id.fingerprint_id
            else:
                fingerprint_id = None
            if id.myanmar_address_obsolete:
                myanmar_address_obsolete = id.myanmar_address_obsolete
            else:
                myanmar_address_obsolete = None
                
            if id.myanmar_address_current:
                myanmar_address_current = id.myanmar_address_current
            else:
                myanmar_address_current = None
            
            if id.b_to_b_sim_no:
                b_to_b_sim_no = id.b_to_b_sim_no
            else:
                b_to_b_sim_no = None
            
            if id.pay_grade:
                pay_grade = id.pay_grade
            else:
                pay_grade = None
            
            if id.number_of_dependents_hr:
                number_of_dependents_hr = id.number_of_dependents_hr
            else:
                number_of_dependents_hr = None
            
            if id.medical_insurance:
                medical_insurance = id.medical_insurance
            else:
                medical_insurance = None
            
            if id.medical_insurance_us:
                medical_insurance_us = id.medical_insurance_us
            else:
                medical_insurance_us = None
            
            if id.dependent_medical_insurance:
                dependent_medical_insurance = id.dependent_medical_insurance
            else:
                dependent_medical_insurance = None
            
            if id.dependent_medical_insurance_us:
                dependent_medical_insurance_us = id.dependent_medical_insurance_us
            else:
                dependent_medical_insurance_us = None
            
            if id.life_insurance:
                life_insurance = id.life_insurance
            else:
                life_insurance = None
            
            if id.life_cover:
                life_cover = id.life_cover
            else:
                life_cover = None
            
            if id.personal_accident:
                personal_accident = id.personal_accident
            else:
                personal_accident = None
            
            if id.personal_accident_cover_us:
                personal_accident_cover_us = id.personal_accident_cover_us
            else:
                personal_accident_cover_us = None
            
            if id.categories:
                categories = id.categories
            else:
                categories = None
                
            if id.housing_allowance:
                housing_allowance = id.housing_allowance
            else:
                housing_allowance = None
            
            if id.education_allowance:
                education_allowance = id.education_allowance
            else:
                education_allowance = None
            
            if id.notice_period_months:
                notice_period_months = id.notice_period_months
            else:
                notice_period_months = None
            
            if id.contract_based:
                contract_based = id.contract_based
            else:
                contract_based = None
            
            if id.assigned_team:
                assigned_team = id.assigned_team
            else:
                assigned_team = None
            
            if id.assigned_category:
                assigned_category = id.assigned_category
            else:
                assigned_category = None
            
            if id.housing_allowance_actual:
                housing_allowance_actual = id.housing_allowance_actual
            else:
                housing_allowance_actual = None
            
            if id.housing_allowance_period_from:
                housing_allowance_period_from = id.housing_allowance_period_from
                housing_allowance_period_from = housing_allowance_period_from.strftime("%Y/%m/%d")
            else:
                housing_allowance_period_from = None
            
            if id.housing_allowance_period_to:
                housing_allowance_period_to = id.housing_allowance_period_to
                housing_allowance_period_to = housing_allowance_period_to.strftime("%Y/%m/%d")
            else:
                housing_allowance_period_to = None
            
            if id.post_paid_ph_card_user:
                post_paid_ph_card_user = id.post_paid_ph_card_user
            else:
                post_paid_ph_card_user = None
            
            
            
            
            sheet.write(row,0,employee_number)
            sheet.write(row,1,cost_center)
            sheet.write(row,2,is_manager)
            sheet.write(row,3,level)
            sheet.write(row,4,whatsapp)
            sheet.write(row,0,b_to_b_sim_no)
            sheet.write(row,6,assign_region)
            sheet.write(row,0,pay_grade)
            sheet.write(row,8,bank_account_local)
            sheet.write(row,9,sin_id)
            sheet.write(row,10,ssb_no)
            sheet.write(row,11,tax_book_no)
            sheet.write(row,12,religion)
            sheet.write(row,13,passport_expiring_date)
            sheet.write(row,14,frc_number)
            sheet.write(row,15,frc_expiring_date)
            sheet.write(row,0,number_of_dependents_hr)
            sheet.write(row,17,number_of_children)
            sheet.write(row,18,medical_insurance)
            sheet.write(row,19,medical_insurance_us)
            sheet.write(row,20,dependent_medical_insurance)
            sheet.write(row,21,dependent_medical_insurance_us)
            sheet.write(row,22,life_insurance)
            sheet.write(row,23,life_cover)
            sheet.write(row,24,personal_accident)
            sheet.write(row,25,personal_accident_cover_us)
            sheet.write(row,26,num_of_dependents)
            sheet.write(row,27,categories)
            sheet.write(row,28,housing_allowance)
            sheet.write(row,29,education_allowance)
            sheet.write(row,30,active)
            sheet.write(row,31,induction_pack_received)
            sheet.write(row,32,fingerprint_id)
            sheet.write(row,33,myanmar_address_obsolete)
            sheet.write(row,34,myanmar_address_current)
            sheet.write(row,35,notice_period_months)
            sheet.write(row,36,contract_based)
            sheet.write(row,37,assigned_team)
            sheet.write(row,38,assigned_category)
            sheet.write(row,39,housing_allowance_actual)
            sheet.write(row,40,housing_allowance_period_from)
            sheet.write(row,41,housing_allowance_period_to)
            sheet.write(row,42,post_paid_ph_card_user)
           
            row = row + 1
        