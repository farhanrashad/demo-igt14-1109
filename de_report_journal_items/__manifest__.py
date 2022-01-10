# -*- coding: utf-8 -*-
{
    'name': "Journal Items Report",
    'summary': """Generate Journal Items Report""",
    'description': """Generate Journal Items Report""",
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'sequence': 1,
    'category': 'Accounting',
    'version': '14.0.0.1',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/account_move_wizard_views.xml',
        'reports/account_move_line_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
