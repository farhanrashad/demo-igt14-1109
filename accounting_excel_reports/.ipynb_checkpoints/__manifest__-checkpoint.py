# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

{
    'name': 'Multi Currency Accounting Excel Report',
    'version': '14.0.2.0.0',
    'category': 'Invoicing Management',
    'summary': 'Contain Following Excel Reports, Partner General Ledger, General Ledger , Trial Balance',
    'sequence': '5',
    'author': 'Dynexcel',
    'company': 'Dynexcel',
    'maintainer': 'Technical Department Dynexcel',
    'support': 'info@dynexcel.com',
    'website': 'https://www.dynexcel.com',
    'license': "OPL-1",
    'price': 300.00,
    'currency': 'USD',
    'website': '',
    'depends': ['accounting_pdf_reports', 'de_account_analytic_default', 'de_account_fin_period'],
    'images': ['static/description/banner.png'],
    'demo': [],
    'data': [
        'reports/report.xml',
        'wizards/account_excel_reports.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
