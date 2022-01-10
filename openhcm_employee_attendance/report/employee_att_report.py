import xlwt

from odoo import models
import datetime

class PartnerXlsx(models.AbstractModel):
    _name = 'report.openhcm_employee_attendance.report_emp_att_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
            all_emp = self.env['hr.employee'].search([])
            all_att = self.env['hr.attendance'].search([('employee_id','=','all_emp[count].id')])
            sheet = workbook.add_worksheet("Employee Attendance Report")
            bold = workbook.add_format({'bold': True})
            sheet.set_column('G:G', 20)
            sheet.set_column('E:E', 15)
            # printing data to excel base on user selection 
            if data['print_by'] == "daily" and data['all_emp']==True :  #if all emp is checked and daily select
                sheet.write('G6', "Employee Attendance", bold)
                current_date=data['current_date']
                print_type="daily : {}".format(current_date)
                sheet.write(6, 6,print_type,bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)
                sheet.write(8, 6,current_date, bold)
                sheet.write(8, 8,"Present", bold)
                sheet.write(8, 9,"Absent", bold)
                row=10
                width=4
                count=0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row,width,all_emp[count].name)
                    # print(all_emp[count].id)
                    all_att = self.env['hr.attendance'].search([('employee_id', '=',all_emp[count].id)])
                    if all_att:
                        count2=0
                        for _ in all_att:
                             user_date=str(all_att[count2].check_in.date())
                             if user_date == current_date:
                                     sheet.write(row, width + 2, "P",bold)
                                     sheet.write(row, width + 4, "1",bold)
                                     sheet.write(row, width + 5, "0",bold)
                                     break;
                             else:
                                sheet.write(row, width + 2, "A",bold)
                                sheet.write(row, width + 4, "0", bold) #present col
                                sheet.write(row, width + 5, "1", bold) #absent col
                             count2+=1
                    else :
                       sheet.write(row, width + 2, "A",bold)
                       sheet.write(row, width + 4, "0", bold)
                       sheet.write(row, width + 5, "1", bold)

                    row=row+1
                    count=count+1
            elif data['print_by'] == 'daily' and data['all_emp']==False: #daily report with checkbox false
                all_emp=data['emp_sel']
                sheet.set_column('F:F', 20)
                sheet.write(5, 5, "Employee Attendance", bold)
                current_date = data['current_date']
                print_type = "daily : {}".format(current_date)
                sheet.write(6, 5, print_type, bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)
                sheet.write(8, 6, current_date, bold)
                sheet.write(8, 8, "Present", bold)
                sheet.write(8, 9, "Absent", bold)
                row = 10
                width = 4
                count = 0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row, width, all_emp[emp])
                    #body of report
                    all_att = self.env['hr.attendance'].search([('employee_id', '=',int(emp))])
                    if all_att:
                        count2 = 0
                        for _ in all_att:
                            user_date = str(all_att[count2].check_in.date())
                            if user_date == current_date:
                                sheet.write(row, width + 2, "P", bold)
                                sheet.write(row, width + 4, "1", bold)
                                sheet.write(row, width + 5, "0", bold)
                                break;
                            else:
                                sheet.write(row, width + 2, "A", bold)
                                sheet.write(row, width + 4, "0", bold)  # present col
                                sheet.write(row, width + 5, "1", bold)  # absent col
                            count2 += 1
                    else:
                        sheet.write(row, width + 2, "A", bold)
                        sheet.write(row, width + 4, "0", bold)
                        sheet.write(row, width + 5, "1", bold)
                    row = row + 1
                    count = count + 1
            elif data['print_by'] == 'weekly' and data['all_emp']==True: #weekly report with checbox true
                sheet.write('G6', "Employee Attendance", bold)
                current_date = data['current_date']
                print_type = "Weekly : {}".format(current_date)
                sheet.write(6, 6, print_type, bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)
                # sheet.write(2, 2, "Employee Name", bold)
                sheet.set_column(2,2,20)
                # sheet.write(8, 6, current_date, bold)
                # printing previous 7 days as weekly print type is selected
                row=8
                width=6
                week_days = 7
                day = 0
                date_str = current_date
                date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                current_date_lst=[]
                for _ in range(week_days):
                    sheet.set_column(row,width, 10)
                    sheet.write(row,width,str(date_object - datetime.timedelta(day)), bold)
                    current_date_lst.append(str(date_object - datetime.timedelta(day)))
                    day += 1
                    width +=1
                    # done printing date for 7 days previous
                sheet.set_column('G:G', 20)
                sheet.write(row, width+1, "Present", bold)
                sheet.write(row, width+2, "Absent", bold)
                row = 10
                width = 4
                count = 0
                emp_present=0
                emp_absent=0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row, width, all_emp[count].name) #for printing name
                    # body report
                    all_att = self.env['hr.attendance'].search([('employee_id', '=', all_emp[count].id)]) #get all record of attendances at employee id
                    width = 6
                    date_found=False
                    for curr_date in current_date_lst: #loop to check week dates

                       if all_att:  #if attendance record is found
                            count2 = 0
                            for _ in all_att: #find matched date in record
                                user_date = str(all_att[count2].check_in.date())
                                if user_date == curr_date:
                                    sheet.write(row, width, "P", bold)
                                    width=width+1;
                                    emp_present+=1
                                    date_found=True
                                    break;
                                count2+=1
                            if not date_found:
                                sheet.write(row, width, "A", bold)
                                emp_absent+=1
                                print("he was absetnt---------------------")
                                width+=1


                       elif not all_att: #attendance record not found
                            sheet.write(row, width, "NF", bold)
                            emp_absent+=1
                            width+=1
                       date_found=False


                    sheet.write(row, width + 1, emp_present, bold)
                    sheet.write(row, width + 2, emp_absent, bold)
                    width = 4
                    # body report ends
                    row = row + 1
                    emp_present = 0
                    emp_absent = 0
                    count = count + 1

            elif data['print_by'] == 'weekly' and data['all_emp'] == False: #weekly report with selected emp
                print("Weekly + selected emp-----------------------")
                all_emp = data['emp_sel']
                sheet.write('G6', "Employee Attendance", bold)
                current_date = data['current_date']
                print(current_date, type(current_date))
                print_type = "Weekly : {}".format(current_date)
                print(print_type)
                sheet.write(6, 6, print_type, bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)                # sheet.write(2, 2, "Employee Name", bold)
                sheet.set_column(2, 2, 20)
                # sheet.write(8, 6, current_date, bold)
                # printing previous 7 days as weekly print type is selected
                row = 8
                width = 6
                week_days = 7
                day = 0
                date_str = current_date
                date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                 # printed in default formatting
                current_date_lst = []
                for _ in range(week_days):
                    sheet.set_column(row, width, 10)
                    sheet.write(row, width, str(date_object - datetime.timedelta(day)), bold)
                    current_date_lst.append(str(date_object - datetime.timedelta(day)))
                    day += 1
                    width += 1
                    # done printing date for 7 days previous
                sheet.set_column('G:G', 20)
                sheet.write(row, width + 1, "Present", bold)
                sheet.write(row, width + 2, "Absent", bold)
                row = 10
                width = 4
                count = 0
                emp_present = 0
                emp_absent = 0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row, width, all_emp[emp])# for printing name
                    # body report
                    all_att = self.env['hr.attendance'].search([('employee_id', '=',int(emp))])  # get all record of attendances at employee id
                    width = 6
                    date_found = False
                    for curr_date in current_date_lst:  # loop to check week dates

                        if all_att:  # if attendance record is found
                            print("user exists ---------", all_att)
                            count2 = 0
                            for _ in all_att:  # find matched date in record
                                user_date = str(all_att[count2].check_in.date())
                                if user_date == curr_date:
                                    sheet.write(row, width, "P", bold)
                                    width = width + 1;
                                    emp_present += 1
                                    date_found = True
                                    break;
                                count2 += 1
                            if not date_found:
                                sheet.write(row, width, "A", bold)
                                emp_absent += 1
                                width += 1


                        elif not all_att:  # attendance record not found
                            sheet.write(row, width, "NF", bold)
                            emp_absent += 1
                            width += 1
                        date_found = False

                    sheet.write(row, width + 1, emp_present, bold)
                    sheet.write(row, width + 2, emp_absent, bold)
                    width = 4
                    # body report ends
                    row = row + 1
                    emp_present = 0
                    emp_absent = 0
                    count = count + 1


            elif data['print_by'] == 'monthly' and data['all_emp'] == True: #monthly report with all emp
                sheet.write('G6', "Employee Attendance", bold)
                current_date = data['current_date']
                print_type = "Monthly : {}".format(current_date)
                print(print_type)
                sheet.write(6, 6, print_type, bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)                # sheet.write(2, 2, "Employee Name", bold)
                sheet.set_column(2, 2, 20)
                # sheet.write(8, 6, current_date, bold)
                # printing previous 7 days as weekly print type is selected
                row = 8
                width = 6
                week_days = 30
                day = 0
                date_str = current_date
                date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                  # printed in default formatting
                # current_date_lst = []
                # for _ in range(week_days):
                #     sheet.set_column(row, width, 10)
                #     sheet.write(row, width, str(date_object - datetime.timedelta(day)), bold)
                #     current_date_lst.append(str(date_object - datetime.timedelta(day)))
                #     day += 1
                #     width += 1
                # trying to print days for months
                current_date_lst = data['days_for_month']
                for _ in range(len(current_date_lst)):
                    sheet.set_column(row, width, 10)
                    sheet.write(row, width, str(current_date_lst[_]), bold)
                    day += 1
                    width += 1

                    # done printing date for 7 days previous
                print("generate list like -----------------",current_date_lst,type(current_date_lst),type(current_date_lst[0]))
                sheet.set_column('G:G', 20)
                sheet.write(row, width + 1, "Present", bold)
                sheet.write(row, width + 2, "Absent", bold)
                row = 10
                width = 4
                count = 0
                emp_present = 0
                emp_absent = 0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row, width, all_emp[count].name)  # for printing name
                    # body report
                    all_att = self.env['hr.attendance'].search(
                        [('employee_id', '=', all_emp[count].id)])  # get all record of attendances at employee id
                    width = 6
                    date_found = False
                    for curr_date in current_date_lst:  # loop to check week dates

                        if all_att:  # if attendance record is found
                            print("user exists ---------", all_att)
                            count2 = 0
                            # present_col=2
                            # absent_col=4
                            for _ in all_att:  # find matched date in record
                                user_date = str(all_att[count2].check_in.date())
                                if user_date == curr_date:
                                    print("User is present on ", curr_date, " while cpmaring date is ", user_date)
                                    sheet.write(row, width, "P", bold)
                                    width = width + 1;
                                    emp_present += 1
                                    date_found = True
                                    break;
                                count2 += 1
                            if not date_found:
                                sheet.write(row, width, "A", bold)
                                emp_absent += 1
                                print("he was absetnt---------------------")
                                width += 1


                        elif not all_att:  # attendance record not found
                            print("record not found for--", all_emp[count].name)
                            sheet.write(row, width, "NF", bold)
                            emp_absent += 1
                            width += 1
                        date_found = False

                    sheet.write(row, width + 1, emp_present, bold)
                    sheet.write(row, width + 2, emp_absent, bold)
                    width = 4
                    # body report ends
                    row = row + 1
                    emp_present = 0
                    emp_absent = 0
                    count = count + 1

            elif data['print_by'] == 'monthly' and data['all_emp'] == False: #monthly report with selected emp
                all_emp = data['emp_sel']
                sheet.write('G6', "Employee Attendance", bold)
                current_date = data['current_date']
                print_type = "Monthly : {}".format(current_date)
                sheet.write(6, 6, print_type, bold)
                sheet.write(8, 3, "S.No", bold)
                sheet.write(8, 4, "Employee", bold)                # sheet.write(2, 2, "Employee Name", bold)
                sheet.set_column(2, 2, 20)
                # sheet.write(8, 6, current_date, bold)
                # printing previous 30 days as monthly print type is selected
                row = 8
                width = 6
                week_days = 30
                day = 0
                date_str = current_date
                date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                 # printed in default formatting
                # current_date_lst = []
                # for _ in range(week_days):
                #     sheet.set_column(row, width, 10)
                #     sheet.write(row, width, str(date_object - datetime.timedelta(day)), bold)
                #     current_date_lst.append(str(date_object - datetime.timedelta(day)))
                #     day += 1
                #     width += 1
                current_date_lst = data['days_for_month']
                for _ in range(len(current_date_lst)):
                    sheet.set_column(row, width, 10)
                    sheet.write(row, width, str(current_date_lst[_]), bold)
                    day += 1
                    width += 1
                    # done printing date for 7 days previous
                sheet.set_column('G:G', 20)
                sheet.write(row, width + 1, "Present", bold)
                sheet.write(row, width + 2, "Absent", bold)
                row = 10
                width = 4
                count = 0
                emp_present = 0
                emp_absent = 0
                for emp in all_emp:
                    sheet.write(row,3,count+1,bold)
                    sheet.write(row, width, all_emp[emp])  # for printing name
                    # body report
                    all_att = self.env['hr.attendance'].search(
                        [('employee_id', '=', int(emp))])  # get all record of attendances at employee id
                    width = 6
                    date_found = False
                    for curr_date in current_date_lst:  # loop to check week dates

                        if all_att:  # if attendance record is found
                            count2 = 0
                            for _ in all_att:  # find matched date in record
                                user_date = str(all_att[count2].check_in.date())
                                if user_date == curr_date:
                                    sheet.write(row, width, "P", bold)
                                    width = width + 1;
                                    emp_present += 1
                                    date_found = True
                                    break;
                                count2 += 1
                            if not date_found:
                                sheet.write(row, width, "A", bold)
                                emp_absent += 1
                                width += 1


                        elif not all_att:  # attendance record not found
                            sheet.write(row, width, "A", bold)
                            emp_absent += 1
                            width += 1
                        date_found = False

                    sheet.write(row, width + 1, emp_present, bold)
                    sheet.write(row, width + 2, emp_absent, bold)
                    width = 4
                    # body report ends
                    row = row + 1
                    emp_present = 0
                    emp_absent = 0
                    count = count + 1

