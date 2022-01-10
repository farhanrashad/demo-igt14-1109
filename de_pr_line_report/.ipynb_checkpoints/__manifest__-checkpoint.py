# -*- coding: utf-8 -*-
{
    'name': "PR Line Report",
    'summary': """Generate PR Line Excel Report""",
    'description': """
        Generate PR Line Report
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",
    'sequence':1,
    'category': 'Agreement',
    'version': '14.0.0.4',
    'depends': ['purchase_requisition','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/view_purchase_requisition.xml',
        'reports/pr_line_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
