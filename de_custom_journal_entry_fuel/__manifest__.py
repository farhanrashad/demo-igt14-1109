# -*- coding: utf-8 -*-
{
    'name': "Fuel Entries",

    'summary': """
        Fuel Custom Entry
        """,

    'description': """
        Fuel Custom Entry:-
        1. Fuel Drawn
        2. Fuel Filling
        
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['de_custom_journal_entry'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/custom_entry_type_views.xml',
        'views/custom_entry_views.xml',
    ],
}
