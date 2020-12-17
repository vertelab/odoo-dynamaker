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
    
    python_code = fields.Text('Price algorithm', default=DEFAULT_PYTHON_CODE,
                        help="Write a Python algorithm that returns the price of the product.")

    dynamaker_product = fields.Boolean(string='Dynamaker Product', default=False)
    
    dynamaker_url = fields.Char(string='Dynamaker URL', size=64, trim=True)

    def _compute_price(self, **kw):
        # construct input to price algorithm
        ldict = {'kw': kw}

        # execute python code with input
        exec(self.python_code, globals(), ldict)
        
        return ldict['price']

class WebsiteProductConfiguratorDynamaker(http.Controller):
    # Handles price update as product parameters are modified
    @http.route(['/product_configurator/dynamaker_price'], type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self, **kw):
        # get product
        product = request.env['product.template'].browse(int(kw.get("product_id")))

        # calculate price
        product.price = product._compute_price(**kw)
        
        return {'price': product.price}
