# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamaker MRP',
    'version': '1.2',
    'category': 'MRP',
    'depends': ['product_configurator_dynamaker', 'mrp'],
    'description': """
Dynamaker: 
========================================================================

Add info here

    """,
    'data': [
    #'views/mrp_production_form_dynamaker.xml',
     'views/product_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
