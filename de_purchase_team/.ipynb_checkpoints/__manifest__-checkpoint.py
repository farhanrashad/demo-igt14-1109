# -*- coding: utf-8 -*-
{
    'name': "Purchase Team",

    'summary': """
        Purchase Team
        """,

    'description': """
Using this application you can manage Purchase Teams with Purchases
=======================================================================
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'purchase/purchase',
    'version': '14.0.0.1',
    'depends': ['base', 'mail','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_team_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
