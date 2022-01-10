# -*- coding: utf-8 -*-
{
    'name': "Production Lot",

    'summary': """
    Unique Lot & OEM Serial
        """,

    'description': """
        Prodction Lot:-
        Unique Lot/Serial No.
        OEM Serial
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['stock','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/stock_lot_data.xml',
        #'data/ir_server_action.xml',
        'views/stock_move_views.xml',
        'views/stock_production_lot_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
