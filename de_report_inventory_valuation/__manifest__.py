# -*- coding: utf-8 -*-

{
    "name": "Inventory Valuation Report",
    'version': '14.0.0.7',
    "category": 'Inventory',
    "summary": ' Inventory Valuation Report',
    'sequence': 1,
    "description": """"Inventory Valuation Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock_account','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_inventory_valuation.xml',
        'wizards/report_inventory_valuation_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

