# -*- coding: utf-8 -*-
{
    'name': "Portal Custom Entry",

    'summary': """
        Portal Custom Entry
        1- Check Custom Entry on Portal
        2- Print Order From Portal
        """,

    'description': """
        Portal Custom Entry
        1- Check Custom Entry on Portal
        2- Print Order From Portal
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal',  'rating', 'resource', 'web', 'web_tour', 'digest', 'de_custom_journal_entry', 'de_custom_journal_entry_import'],

    # always loaded
    'data': [
        'wizard/correction_reason_views.xml',
        'security/ir.model.access.csv',
        'views/custom_entry_views.xml',
        'views/custom_entry_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
