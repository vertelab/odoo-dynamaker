# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, http, models, tools, _

class ProductTemplate(models.Model):
    _inherit = "product.template"
    dynamaker_url = fields.Char(string='Dynamaker url', size=64, trim=True, )

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
