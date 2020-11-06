# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv import expression
from odoo.tools import html2plaintext
from odoo.tools.misc import get_lang

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    dynamaker_url = fields.Char(string='Dynamaker url', size=64, trim=True)

class WebsiteProductConfiguratorDynamaker(http.Controller):
    @http.route(['/product_configurator/dynamaker_price'], type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self, **kw):
        width = kw.get('width')
        length = kw.get('length')
        thickness = kw.get('thickness')
        edgeType = kw.get('edgeType')
        
        _logger.warn("~ width: %s " % width)
        _logger.warn("~ length: %s " % length)
        _logger.warn("~ thickness: %s " % thickness)
        _logger.warn("~ edge: %s " % edgeType)

        price = self.calcProductPrice(width, length, thickness, edgeType)
        
        return request.website.viewref('product.product_template_form_view').render({'price': price})

    def calcProductPrice(self, x, y, z, edgeType):
        edgeTypeCost = 0
        
        if edgeType == "polished":
            edgeTypeCost = 50
        elif edgeType == "standard":
            edgeTypeCost = 15
            
        # price = 0.5$ per cm³ + edgeType
        return x*y*z/50 + edgeTypeCost;
