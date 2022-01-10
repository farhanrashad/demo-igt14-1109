# -*- coding: utf-8 -*-
{
    'name': "Project Pricing",

    'summary': """
        Project Pricing
        """,

    'description': """
        Pricing for Project
        - Fuel 
        - Electrcity 
        - etc
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/pricelist_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
