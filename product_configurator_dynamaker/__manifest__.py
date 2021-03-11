# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamaker',
    'version': '1.2',
    'category': 'Sales/Sales',
    'depends': ['website_sale'],
    'description': """
Dynamaker: Parametric Product Customization
========================================================================

Build and Publish Your Own Online Visual CAD Configurators that automatically can generate 3D-files, BOM-lists, 2D drawings and manufacturing data for every quotation and order.

    """,
    'data': [
        'views/product_views.xml',
        'views/lukas_variant_templates.xml'
    ],
    'installable': True,
    'auto_install': False,
}
