# -*- coding: utf-8 -*-
{
    'name': "Purchase Pricelist",

    'summary': """
        Purchase Pricelist
        """,

    'description': """
        Purchase Pricelist
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '14.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','de_project_planning'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_pricelist_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
