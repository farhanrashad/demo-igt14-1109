# -*- coding: utf-8 -*-
{
    'name': "Account Stock Transfer",
    'summary': """
        Account Stock Transfer
        """,
    'description': """
        Stock Transfer:-
        Bill to Receipt
        Invoice to Delivery
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.0.1',
    'depends': ['base','stock','account'],
    'data': [
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
    ],
}

