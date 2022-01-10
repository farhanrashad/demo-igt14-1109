# -*- coding: utf-8 -*-
{
    'name': "Operations",

    'summary': """
    Operations - Accounting
        """,

    'description': """
        Operations:-
        purchase Subscription
        Sale Subscription
        Customized 
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['de_purchase_subscription','de_project_planning','de_custom_journal_entry'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'data/operations_data.xml',
        'views/operations_menu_views.xml',
        #'views/purchase_configuration_views.xml',
        #'views/sale_configuration_views.xml',
        #'views/purchase_subscription_type_views.xml',
        #'views/purchase_subscription_views.xml',
        #'views/sale_subscription_type_views.xml',
        #'wizard/purchase_subscription_adjustments_views.xml',
        #'wizard/purchase_subscription_plan_views.xml',
        #'views/purchase_agreements_views.xml',
        #'views/purchase_agreements_deductions_views.xml',
        'views/custom_journal_entry_views.xml',
        'views/project_views.xml',
        #'wizard/custom_entry_advance_inv_wizard_views.xml',
        #'views/custom_entry_views.xml',
        #'views/sale_agreements_views.xml',
        #'views/stock_fuel_views.xml',
        #'views/account_journal_views.xml',
        #'views/account_move_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
