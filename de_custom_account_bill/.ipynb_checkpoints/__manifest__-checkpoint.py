# -*- coding: utf-8 -*-
{
    'name': "Custom Accounting Bills",
    'summary': """
    Vendor Bills
    """,
    'sequence': '1',
    'description': """
    Custom Accounting Bills:-
    Electricity Bills
    """,
    'category': 'Accounting',
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'version': '14.0.0.1',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/custom_bill_data.xml',
        'views/custom_bill_type_views.xml',
        'views/custom_account_bill_views.xml',
    ],
    'demo': [
    ],
    'images': [
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
