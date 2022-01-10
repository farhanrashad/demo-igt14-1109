# -*- coding: utf-8 -*-
{
    'name': "Portal Hoto Site",

    'summary': """
        Portal Hoto Site task
        """,

    'description': """
        Portal Hoto Site task
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '14.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','project','de_operations'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
#         'views/project_project_views.xml',
        'views/project_task_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
