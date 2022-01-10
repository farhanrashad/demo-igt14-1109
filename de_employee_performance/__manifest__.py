# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Performance",
    "category": 'Employee',
    "summary": 'Employee Performance Evaluation',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['base','project'],
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/appraisal_view.xml',
        'views/appraisal_inh_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
