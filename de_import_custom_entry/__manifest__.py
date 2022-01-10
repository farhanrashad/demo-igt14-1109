# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Entry From CSV/Excel File",
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    "support": "support@dynexcel.com",
    "version": "14.0.0.1",
    "category": "Warehouse",
    "license": "OPL-1",
    "summary": "Import lot picking From CSV, Import lot picking from Excel,Import serial picking from csv, Import serial picking from Excel import picking from XLS, Import pickings From XLSX,Import Serial Number,import Lot Number,import lot serial in picking Odoo",
    "description": """This module imports lot/serial picking from CSV/Excel files in a single click. You can transfer a lot/serial pickings from one location to other locations. When you transfer lot/serial picking, you have the option to create a lot/serial on the destination location. You can import custom fields from CSV or Excel.""",
    "depends": [
        'de_custom_journal_entry',
        'sh_message',
    ],
    "data": [
        #'security/import_lot_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_line_wizard.xml',
        'views/custom_entry_type_views.xml',
        'views/custom_entry_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "30",
    "currency": "EUR"
}
