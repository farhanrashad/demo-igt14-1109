# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

{
    "name": "Account Fixed Discount",
    "summary": "Allows to apply fixed amount discounts in invoices.",
    "version": "14.0.1.1",
    "category": "Accounting",
    "website": "https://dynexcel.com",
    "author": "Dynexcel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account"],
    "data": [
        "views/account_move_view.xml", 
        "reports/report_account_invoice.xml"
    ],
}
