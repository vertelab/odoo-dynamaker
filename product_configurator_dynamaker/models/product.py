# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
#import re

from odoo import api, fields, models, tools, _
#from odoo.exceptions import ValidationError
#from odoo.osv import expression
#from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    dynamaker_url = fields.Char(string='Dynamaker url', size=64, trim=True)
    
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
    @http.route(['/product_configurator/dynamaker_price'], type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self):
        #domain = request.website.website_domain()
        #return request.website.viewref('product.product_template_form_view').render({'data': 200, 'value': 201, 'domains': domain, 'open_cfg_step_line_ids': None, 'config_image_vals': None})
        return request.website.viewref('product.product_template_form_view').render({'price': self.calcProductPrice(0, 0, 0), 'edge-type': None})

    def calcProductPrice(self, x, y, z):
        return x*y*z;
