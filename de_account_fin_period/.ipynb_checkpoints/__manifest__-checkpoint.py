# -*- coding: utf-8 -*-
{
    'name': "Financial Period",

    'summary': """
        Financial Period
        """,

    'description': """
        Financial Period
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Dynexcel',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
