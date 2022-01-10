# -*- coding: utf-8 -*-
{
    'name': "Internal Requisition-Stock Transfer",

    'summary': """
    Material Requisition - (Internal) 
        """,

    'description': """
Stock Material Transfer
=============================================
        1 - Transfer Requests
        2 - Material Transfer
        3 - Material replacement
        4 - Dependency on transfer order
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Warehouse',
    'version': '14.0.6.2',
    'depends': ['base', 'stock','stock_barcode','purchase','purchase_stock','account','project'],
    'data': [
        'security/requisition_security.xml',
        'security/ir.model.access.csv',
        'data/requisition_data.xml',
        'views/stock_requisition_menu.xml',
        'views/stock_transfer_order_category_views.xml',
        'views/stock_transfer_order_type_views.xml',
        'views/stock_transfer_order_stage_views.xml',
        'views/stock_transfer_exception_type_views.xml',
        'views/stock_transfer_material_condition_views.xml',
        'views/stock_transfer_close_reason_views.xml',
        'wizard/stock_transfer_close_reason_wizard_views.xml',
        #'wizard/cma_order_replace_wizard_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_transfer_order_views.xml',
        'wizard/stock_transfer_scheduler_wizard_views.xml',
    ],
}
