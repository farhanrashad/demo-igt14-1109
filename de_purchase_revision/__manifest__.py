# -*- encoding: utf-8 -*-
{
	"name": "Purchase Revision History",
	"version": "12.0",
	"author": "Dynexcel",
	"website": "https://www.dynexcel.com",
	"sequence": 0,
	"depends": ["purchase","purchase_stock",],
	"category": "Purchase",
	"complexity": "easy",
	'license': 'LGPL-3',
    'support': 'info@dynexcel.com',
	"description": """
Purchase Order revision history
	""",
	"data": [
		'views/purchase_order_views.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/banner.jpg'],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
