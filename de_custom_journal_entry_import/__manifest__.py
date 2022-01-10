# -*- coding: utf-8 -*-
{
    'name': "Import Third Party Bills",

    'summary': """
        Import Third Party Bills  from task
        """,

    'description': """
        Import Third Party Bills  from task
    """,

    'author': "Dynexecel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '14.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'de_custom_journal_entry', 'website_form'],

    # always loaded
    'data': [
        'data/ir_server_action.xml',
        'wizard/custom_entry_wizard.xml',
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/account_custom_entry_view.xml',
        'views/custom_entry_type_views.xml',
        'views/project_task_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
