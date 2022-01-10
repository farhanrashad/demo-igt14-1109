# -*- coding: utf-8 -*-
###################################################################################
{
    'name': 'Employee Overtime',
    'version': '14.0.0.5',
    'summary': 'Manage Employee Overtime',
    'description': """
        Helps you to manage Employee Overtime. 
        """,
    'category': 'Human Resources',
    'author': "Dynexcel",
    'live_test_url': 'https://youtu.be/lOQCTCxrUKs',
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': "https://www.dynexcel.com",
    'depends': [
        'base','hr', 'hr_contract', 'hr_holidays','hr_payroll', 'hr_attendance','project','hr_recruitment'
    ],
    
    'data': [

        'security/ir.model.access.csv',
        'data/data.xml',
        'views/overtime_menu.xml',
        #'views/res_config_settings_views.xml',
        'views/overtime_type_views.xml',
        'views/hr_contract_views.xml',
        'views/overtime_request_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_employee_views.xml',
        
    ],
    #'demo': ['data/hr_overtime_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
