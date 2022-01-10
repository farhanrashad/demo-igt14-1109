# -*- coding: utf-8 -*-

{
    "name": "Tax Ledger",
    'version': '14.0.0.1',
    "category": 'Accounting',
    "summary": 'Tax Ledger',
    'sequence': 1,
    "description": """" Tax Ledger """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['account','report_xlsx','de_account_fin_period','de_account_analytic_default'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_tax_ledger.xml',
        'wizards/report_tax_ledger_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

