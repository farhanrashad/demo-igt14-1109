# -*- coding: utf-8 -*-
{
    'name': "HR Employee Details Report",
    'summary': """Generate HR Employee Details Report""",
    'description': """
        Generate HR Employee Details Report
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",
    'sequence':1,
    'category': 'Human Resource',
    'version': '14.0.0.2',
    'depends': ['hr','account','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/employee_details_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
