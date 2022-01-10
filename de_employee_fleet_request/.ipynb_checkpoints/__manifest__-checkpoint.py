# -*- coding: utf-8 -*-

{
    "name": "Fleet (ESS)",
    "category": 'Employee',
    "summary": 'Fleet Vehicle Request by Employee',
    "description": """
         Fleet Vehicle Request by Employee
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['base','hr','fleet','project'],
    "data": [
         
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/fleet_request_report.xml',
        'report/fleet_request_report_pdf.xml',
        'wizard/vehicle_request_wizard_view.xml',
        'views/fleet_request_view.xml',
        'views/service_category.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}