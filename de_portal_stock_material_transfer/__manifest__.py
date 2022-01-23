# -*- coding: utf-8 -*-
{
    'name': "Portal Stock Material Transfer",

    'summary': """
        Portal Stock Material Transfer
        """,

    'description': """
        Portal Stock Material Transfer
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','de_stock_material_transfer'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_transfer_templates.xml',
        'views/stock_transfer_views.xml',
        'views/stock_transfer_category_views.xml',
        'views/stock_transfer_type_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
