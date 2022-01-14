# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamaker MRP',
    'version': '1.2',
    'category': 'MRP',
    'depends': ['product_configurator_dynamaker', 'mrp'],
    'description': """
Dynamaker extension to the mrp module

    """,
    'data': [
     'views/product_views.xml',
    ],
    'demo': ['data/dynamaker_demo.xml'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
