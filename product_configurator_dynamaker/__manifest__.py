# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Dynamaker Webshop',
    'version': '1.2',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Dynamaker: Parametric Product Customization',
    'category': 'Production',
    'description': """
Dynamaker: Parametric Product Customization
========================================================================

Build and Publish Your Own Online Visual CAD Configurators that automatically can generate 3D-files, BOM-lists, 2D drawings and manufacturing data for every quotation and order.

    """,
    #'sequence': '1'
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-dynamaker/product_configurator_dynamaker',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-dynamaker',

    'depends': ['website_sale', 'sale_management'],
    'data': [
        'views/product_views.xml',
        'views/dynamaker_website_sale.xml'
    ],
    'demo': ['data/dynamaker_demo.xml'],
    'installable': True,
    'auto_install': False,
}
