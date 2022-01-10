# -*- coding: utf-8 -*-

{
    "name": "GDN/GTN Report",
    'version': '14.0.0.2',
    "category": 'Inventory',
    "summary": ' GDN/GTN Report',
    'sequence': 1,
    "description": """"GDN/GTN Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_stock_material_transfer','project','de_secondary_currency'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_transfer_picking.xml',
        'wizards/report_transfer_picking_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

