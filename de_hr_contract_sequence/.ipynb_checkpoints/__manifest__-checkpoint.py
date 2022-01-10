# -*- coding: utf-8 -*-
{
    'name': "Contact Sequence",

    'summary': """
        Contact Sequence
        """,

    'description': """
        Contact Sequence
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/contract_data.xml',
        'views/hr_contract_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
