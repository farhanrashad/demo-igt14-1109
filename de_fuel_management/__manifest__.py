# -*- coding: utf-8 -*-
{
    'name': "Fuel Management",

    'summary': """
        Location wise Fuel Management
        """,

    'description': """
        Location wise Fuel Management
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/stock_refill_menu.xml',
        'views/stock_location_views.xml',
        'views/stock_refill_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
