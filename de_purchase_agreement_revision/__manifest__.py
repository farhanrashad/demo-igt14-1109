# -*- encoding: utf-8 -*-
{
	"name": "Purchase Agreement Revision History",
	"version": "14.0.0.1",
	"author": "Dynexcel",
	"website": "https://www.dynexcel.com",
	"sequence": 0,
	"depends": ["purchase_requisition","purchase_requisition_stock",],
	"category": "Purchase",
	"complexity": "easy",
	'license': 'LGPL-3',
    'support': 'info@dynexcel.com',
	"description": """
Purchase Agreement revision history
	""",
	"data": [
		'views/purchase_requisition_views.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/banner.png'],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
