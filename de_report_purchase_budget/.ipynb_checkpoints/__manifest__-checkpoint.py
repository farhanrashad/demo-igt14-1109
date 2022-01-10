# -*- coding: utf-8 -*-
{
    'name': "Purchase Budget Report",

    'summary': """
        Purchase Budget Report
        """,

    'description': """
       Purchase Budget Report
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '14.0.0.6',

    # any module necessary for this one to work correctly
    'depends': ['base','de_purchase_budget','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/report_purchase_budget.xml',
    ],
}

