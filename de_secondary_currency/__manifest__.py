# -*- coding: utf-8 -*-
{
    'name': "Secondary Currency",

    'summary': """
        Secondary Currency
        """,

    'description': """
        Secondary Currency
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account/Purchase',
    'version': '14.0.1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase_requisition','stock','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/res_company_views.xml',
        'views/account_move_views.xml',
        'views/purchase_views.xml',
        'views/purchase_requisition_views.xml',
        'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
