# -*- coding: utf-8 -*-

{
    "name": "Account Statement Report",
    'version': '14.0.0.5',
    "category": 'Accounting',
    "summary": ' Account Statement Report',
    'sequence': 1,
    "description": """"Account Statement Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['report_xlsx','account'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_acc_statement.xml',
        'wizards/report_acc_statement_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

