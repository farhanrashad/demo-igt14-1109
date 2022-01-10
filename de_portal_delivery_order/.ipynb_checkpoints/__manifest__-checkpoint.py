# -*- coding: utf-8 -*-
{
    'name': "Portal Delivery Order",

    'summary': """
        Portal Delivery Order
        1- Check Delivery Order on Portal
        2- Print Order From Portal
        """,

    'description': """
        Portal Delivery Order
        1- Check Delivery Order on Portal
        2- Print Order From Portal
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal',  'rating', 'resource', 'web', 'web_tour', 'digest'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
