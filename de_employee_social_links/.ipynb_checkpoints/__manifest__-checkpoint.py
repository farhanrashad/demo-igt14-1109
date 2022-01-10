# -*- coding: utf-8 -*-
{
    'name': "Employee Social Links",

    'summary': """
        Employee Social Links By Dynexcel""",

    'description': """
        1. Add Employee Social Links to Employee Form
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'HR',
    'version': '14.0.1.1',
    "sequence": 7,
    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/social_link_view.xml',
    ],
    # only loaded in demonstration mode
    "installable": True,
    "application": True,
    "auto_install": False,
}
