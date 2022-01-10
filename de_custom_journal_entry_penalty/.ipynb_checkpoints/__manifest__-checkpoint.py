# -*- coding: utf-8 -*-
{
    'name': "Operations Penalties",

    'summary': """
        Operations Penalties
        """,

    'description': """
        Operations Penalties:-
        1. SLA Penalty
        2. PM Penalty
        3. Materail Penalty
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['de_custom_journal_entry','de_custom_journal_entry_om'],

    # always loaded
    'data': [
        'security/penalty_security.xml',
        'security/ir.model.access.csv',
        'views/penalty_menu.xml',
        'views/penalty_config_views.xml',
        'views/custom_entry_type_views.xml',        
        'views/custom_entry_views.xml',
    ],
}
