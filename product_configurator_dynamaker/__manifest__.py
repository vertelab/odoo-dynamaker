# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamaker Webshop',
    'version': '1.2',
    'category': 'Sales/Sales',
    'depends': ['website_sale', 'sale_management'],
    'description': """
Dynamaker: Parametric Product Customization
========================================================================

Build and Publish Your Own Online Visual CAD Configurators that automatically can generate 3D-files, BOM-lists, 2D drawings and manufacturing data for every quotation and order.

    """,
    'data': [
        'views/product_views.xml',
        'views/dynamaker_website_sale.xml'
    ],
    'demo': ['data/dynamaker_demo.xml'],
    'installable': True,
    'auto_install': False,
}
