# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Fleet Fuel",
    "category": 'Fleet',
    "summary": 'Fleet Fuel Summary',
    "description": """
	 This module is related to fleet fuel tank
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['sale','fleet'],
    "data": [
        'security/ir.model.access.csv',
        'wizards/fleet_fuel.xml',
        'views/fleet_fuel_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}