# -*- coding: utf-8 -*-
{
    'name': "OM Invoices",

    'summary': """
        OM Invoices
        """,

    'description': """
        OM Invoices:-
        
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.1.4',

    # any module necessary for this one to work correctly
    'depends': ['de_custom_journal_entry'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/custom_entry_type_views.xml',
        'wizard/custom_entry_wizard_inv_views.xml',
        'views/custom_entry_views.xml',
        'views/custom_entry_stage_views.xml'
        
    ],
}
