# -*- coding: utf-8 -*-
{
    'name': "Account Analytic Default",

    'summary': """
    Account Analytic Default
        """,

    'description': """
        Account Analytic Default:-
        - Project
        - Department
        - Employee
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Human Resource/Account',
    'version': '14.0.0.2',
    'depends': ['base','hr','account','project','analytic'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_analytic_default_views.xml',
        'views/account_analytic_line_views.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
