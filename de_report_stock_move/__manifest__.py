# -*- coding: utf-8 -*-

{
    "name": "Stock Move Report",
    'version': '14.0.0.4',
    "category": 'Inventory',
    "summary": ' Stock Move Report',
    'sequence': 1,
    "description": """"Stock Move Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_stock_material_transfer','project'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_stock_move.xml',
        'wizards/report_stock_move_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

