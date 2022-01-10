# -*- coding: utf-8 -*-
{
    'name': "Fleet Entries",

    'summary': """
        Fleet Entries
        """,

    'description': """
        Fleet Entries
        
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['de_custom_journal_entry'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/custom_entry_type_views.xml',
        'views/custom_entry_views.xml',
    ],
}
