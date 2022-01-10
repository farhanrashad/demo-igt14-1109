# -*- coding: utf-8 -*-
{
    'name': "Account Bill Tax",
    'summary': """
        Account Bill Tax
        """,
    'description': """
        Account Bill Tax
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.0.3',
    'depends': ['account'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_views.xml',
        'views/account_tax_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
