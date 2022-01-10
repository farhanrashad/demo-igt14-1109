# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Promotion",
    "category": 'HR',
    "summary": 'Employee Promotion Summary',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['hr','base','hr_payroll'],
    "data": [
        'security/ir.model.access.csv',
        'reports/employee_promotion_template.xml',
        'reports/employee_promotion_report.xml',
        'views/employee_view.xml',
        'views/employee_menu.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}