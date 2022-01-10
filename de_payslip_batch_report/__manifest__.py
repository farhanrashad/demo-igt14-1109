# -*- coding: utf-8 -*-
{
    'name': "Payslip Batch Report",
    'summary': """Generate PaySlip Batch Excel Report""",
    'description': """Generate PaySlip Batch Report""",
    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",
    'sequence': 1,
    'category': 'Payroll',
    'version': '14.0.0.1',
    'depends': ['base', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/payslip_batch.xml',
        'views/view_payslip_batch.xml',
        'reports/payslip_batch_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
