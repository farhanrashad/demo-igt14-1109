# -*- coding: utf-8 -*-
{
    'name': "Extended Addresses",

    'summary': """
    Add extra fields on addresses
        """,

    'description': """
Extended Addresses Management
=============================

This module holds extra fields for contact like:
District
Sub-district
Township.
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Uncategorized',
    'version': '14.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base_address_city','contacts'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_country_district_views.xml',
        'views/res_country_views.xml',
        'views/res_city_town_views.xml',
        'views/res_city_views.xml',
        'views/res_partner_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
