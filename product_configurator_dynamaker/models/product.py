# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)

class DynamakerProductAttribute(models.Model):
    _inherit = "product.attribute"

    display_type = fields.Selection(selection_add=[('hidden_text', 'Hidden Text')])

class DynamakerProductTemplate(models.Model):
    _inherit = "product.template"
    
    DEFAULT_PYTHON_CODE = """# Specify the python price algorithm.
#  - Access the product attributes through the 'kw' dict, eg. kw['width'], and kw['length'].
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
        # TODO: get id of product through kw? Below is temporary id for Customizable Desk (CONFIG).
        PRODUCT_ID = 9
        
        # get product
        product = request.env['product.template'].browse(PRODUCT_ID)
        
        #_logger.warn("~ %s" % product.product_template_attribute_value_ids.mapped("name"))
        
        # calculate price
        price = product._compute_price(**kw)
        
        return {'price': price}

        
        
        
        
