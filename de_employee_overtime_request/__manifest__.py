#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Over time request with Payroll',
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
        'views/overtime_request.xml',
    ],
    
}
