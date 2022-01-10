# -*- coding: utf-8 -*-
{
    'name': "Third-Party Billing",
    'summary': """
        Third Party Billing
        """,
    'description': """
        Third Party Billing
        - Admin
        - Fleet
        - Travel
        - Electricity
        - Fuel
        
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'version': '14.0.7.6',
    
    'depends': ['base','de_purchase_subscription','account', 'analytic', 'fleet', 'de_project_planning','project','stock','purchase_requisition','purchase','de_stock_material_transfer'],

    # always loaded
    'data': [
        'security/entry_security.xml',
        'security/ir.model.access.csv',
        'views/custom_entry_menu.xml',
        'views/custom_entry_type_views.xml',
        'views/custom_entry_stage_views.xml',
        'views/account_move_views.xml',
        'views/custom_entry_views.xml',
        'views/account_payment_views.xml',
    ],
}
