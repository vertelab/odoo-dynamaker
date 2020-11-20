# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    DEFAULT_PYTHON_CODE = """# Specify the python price algorithm here.
#  - Just set the price variable, e.g. price = kw['width'] * kw['length'].
#\n\n\n\n"""
    
    python_code = fields.Text('Price Algorithm', default=DEFAULT_PYTHON_CODE,
                        help="Write a Python algorithm that returns the price of the product.")
    
    dynamaker_url = fields.Char(string='Dynamaker url', size=64, trim=True)

    def _compute_price(self, **kw):
        ldict = {'kw': kw}
        
        # TODO: ensure code is safe
        exec(self.python_code, globals(), ldict)
        
        price = ldict['price']

        return price

class WebsiteProductConfiguratorDynamaker(http.Controller):
    # Handles price update as product parameters are modified
    @http.route(['/product_configurator/dynamaker_price'], type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self, **kw):
        # TODO: get id of product through kw. Below is temporary id for Customizable Desk (CONFIG).
        PRODUCT_ID = 9 
    
        # get product
        product = request.env['product.template'].browse(PRODUCT_ID)
        
        # calculate price
        price = product._compute_price(**kw)
        
        return {'price': price}
    
    # Middle hand before product is added to cart: Adds product attributes to order line before proceeding
    @http.route(['/product_configurator/add_to_cart'], type='json', auth='public', website=True)
    def add_product_to_cart(self, **kw):
        PRODUCT_ID = 9 
        add_qty = 1
        set_qty = 0
        
        # /usr/share/core-odoo/addons/website_sale/controllers/main.py:420
        request.env['sale.order'].cart_update(PRODUCT_ID, add_qty, set_qty, kw)
        
        _logger.warn("~ DONE! orderrads extra attribut = %s" % sale_order_line.product_custom_attribute_value_ids)

# create a sale.order.line if not already exist (TODO: else update)
#sale_order_line = request.env['sale.order.line'].create({'order_id': ORDER_ID, 'name': product.name, 'price_unit': price, 'product_uom_qty': 1, 'customer_lead' : 99999})

# create that sale_order_line's product_custom_attribute_value_ids
#for attribute, value in kw.items():
#    sale_order_line.product_custom_attribute_value_ids.write((0, _, {'sale_order_line_id': sale_order_line.id, 'name': attribute, 'custom_value': value}))
        
