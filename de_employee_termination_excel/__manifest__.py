# -*- coding: utf-8 -*-
{
    'name': "Employee Termination Report",

    'summary': """
        Employee Termination Reports PDF and Excel.
        """,

    'description': """
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    'category': 'HR',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/employee_termination_wizard.xml',
        'views/menu.xml',
        'report/termination_template_pdf.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
