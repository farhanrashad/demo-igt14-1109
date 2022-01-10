# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Lot-Serial Picking From CSV/Excel File",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "14.0.1",
    "category": "Warehouse",
    "license": "OPL-1",
    "summary": "Import lot picking From CSV, Import lot picking from Excel,Import serial picking from csv, Import serial picking from Excel import picking from XLS, Import pickings From XLSX,Import Serial Number,import Lot Number,import lot serial in picking Odoo",
    "description": """This module imports lot/serial picking from CSV/Excel files in a single click. You can transfer a lot/serial pickings from one location to other locations. When you transfer lot/serial picking, you have the option to create a lot/serial on the destination location. You can import custom fields from CSV or Excel.""",
    "depends": [
        'stock',
        'sh_message',
    ],
    "data": [
        'security/import_lot_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_lot_wizard.xml',
        'views/stock.xml',
    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "30",
    "currency": "EUR"
}
