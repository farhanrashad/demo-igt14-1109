# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Extra Info",
    "category": 'Employee',
    "summary": 'Employee Extra Information',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['base','hr'],
    "data": [
        'security/ir.model.access.csv',
        'views/extra_info_view.xml',
        'views/extra_info_view_inh.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
