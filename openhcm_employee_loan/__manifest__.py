{
    'name': 'openhcm_employee_loan',
    'category': 'Human Resources',
    'version': '13.0.1.0.0',
    'author': 'dynexcel',
    'summary': 'Daily life work',
    'description': "",
    'depends': [
         'hr',
        'hr_payroll',
        'base',

    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hr_payslip_view.xml',
        'views/employee_loan.xml',
    ],
    
}
