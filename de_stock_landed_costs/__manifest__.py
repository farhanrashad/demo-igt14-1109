# -*- coding: utf-8 -*-
{
    'name': "Landed Cost",

    'summary': """
    Extend Landed Cost
        """,

    'description': """
        Extend Landed Cost
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    'category': 'Warehouse/Purchase',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['stock_landed_costs'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/landed_cost_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
