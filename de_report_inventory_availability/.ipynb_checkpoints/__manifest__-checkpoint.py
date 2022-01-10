# -*- coding: utf-8 -*-

{
    "name": "Inventory Availability Report",
    'version': '14.0.0.6',
    "category": 'Inventory',
    "summary": ' Inventory Availability Report',
    'sequence': 1,
    "description": """"Inventory Availability Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock_account','report_xlsx','de_stock_material_transfer'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_inventory_availability.xml',
        'wizards/report_inventory_availability_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

