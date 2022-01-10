# -*- coding: utf-8 -*-
{
    'name': "Travel Request",
    'summary': """Travel Request""",
    'description': """ """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
    'category': 'Hr',
    'version': '14.0.0.0',
    'depends': ['base', 'hr','digest'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/ticket_allocation_view.xml',
        'views/ticket_balance_view.xml',
        'views/travel_request_view.xml',
        'views/travel_request_menu.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
