# -*- coding: utf-8 -*-

{
    "name": "Account Aging",
    'version': '14.0.0.1',
    "category": 'Accounting',
    "summary": ' Customer Aging Report',
    'sequence': 1,
    "description": """"Account Aging Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['account','report_xlsx',],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_account_aging.xml',
        'wizards/report_account_aging_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

