# -*- coding: utf-8 -*-
# Copyright (C) 2020 Vertel AB
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dynamic_attribute_ids = fields.One2many(comodel_name='product.dynamic.attribute',inverse_name='product_id',string='Dynamic Attribute',help="Names on attribute types for this product template") # 

class ProductDynamicAttribut(models.Model):
    _name = 'product.dynamic.attribute'

    name = fields.Char(string='Attribute', size=64, trim=True, )
    product_id = fields.Many2one(comodel_name='product.template',string='Product') 
    type = fields.Selection(selection=[('int','Integer'),('float','Float'),('img','Image')],string='Type')
    int_max = fields.Integer(string='Max')
    int_min = fields.Integer(string='Min')
    float_max = fields.Float(string='Max')
    float_min = fields.Float(string='Min')
    # ~ image = fields.Binary(string='Image',attachment=True)



class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    pass
    compute_price = None

class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def get_product_price(self, product, quantity, partner, date=False, uom_id=False):
        """ For a given pricelist, return price for a given product """
        self.ensure_one()
        # context with sale-order-line  
        # super().get_product_price()
        return self._compute_price_rule([(product, quantity, partner)], date=date, uom_id=uom_id)[product.id][0]

