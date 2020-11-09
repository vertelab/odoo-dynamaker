# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    dynamaker_url = fields.Char(string='Dynamaker url', size=64, trim=True, )

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

class WebsiteProductConfiguratorDynamaker(http.Controller):
    @http.route(['/product_configurator/dynamaker_price'],
                 type='json',
                 auth='public',
                 website=True)
    def product_configurator_dynamaker_price(self, **kw):
        width = kw.get('width')
        length = kw.get('length')
        thickness = kw.get('thickness')
        edgeType = kw.get('edgeType')

        price = self.getProductPrice(width, length, thickness, edgeType)
        
        return {'price': price}

    def getProductPrice(self, x, y, z, edgeType):
        edgeTypeCost = 0
        
        if edgeType == "polished":
            edgeTypeCost = 50
        elif edgeType == "standard":
            edgeTypeCost = 15
            
        # price = 0.5$ per cm³ + edgeType
        return round(x*y*z/900000) + edgeTypeCost;
