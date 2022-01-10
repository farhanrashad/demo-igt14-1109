# -*- coding: utf-8 -*-

{
    "name": "Spare Part Penalty Report",
    'version': '14.0.0.1',
    "category": 'Inventory',
    "summary": ' Spare Part Penalty Report',
    'sequence': 1,
    "description": """"Spare Part Penalty Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_stock_material_transfer','project'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_spare_penalty.xml',
        'wizards/report_spare_penalty_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

