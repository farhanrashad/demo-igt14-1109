#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Request Job Position Workflow',
    'category': 'Human Resources',
    'version': '13.0.1.0.0',
    'author': 'Dynexcel',
    'summary': 'Employee can create request for new Job Position',
    'description': "Odoo Application allows employees to create Job Position Request, "
                   "once request is approved by Recruitment Manager then requested Job Position "
                   "will be created and after that usual recruitment process can take place",
    'depends': [
        'hr',
        'hr_recruitment',
        'base',
        'mail',
    ],
    'data': [
        'data/sequence.xml',
        'data/email_template.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/job_request.xml',
        'views/hr_applicant.xml',
        'views/hr_job_view.xml',
    ],
    
}
