# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "COS Connector",
    "category": 'Integration',
    "summary": 'Click On Site Integration',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['product'],
    "data": [
        'security/ir.model.access.csv',
#         'security/training_security.xml',
        'views/cos_view.xml',
        'views/material_request_form.xml',
        'views/product_view.xml',
        'views/cos_menu.xml',
#         'report/employee_report_pdf.xml',
    ],
    
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
