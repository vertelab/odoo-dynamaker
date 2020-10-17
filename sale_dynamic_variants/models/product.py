# -*- coding: utf-8 -*-
# Copyright (C) 2020 Vertel AB
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dynamic_variant_ids = fields.One2many(comodel_name='product.dynamic.variant',inverse_name='product_id',string='Dynamic Variants',help="Names on variant types") # 

class ProductDynamicVariants(models.Model):
    _name = 'product.dynamic.variant'

    name = fields.Char(string='Dynamic Variant', size=64, trim=True, )
    product_id = fields.Many2many(comodel_name='product.template',string='Product') 
    # type = fields.Selection(selection=[('int','Integer'),('float','Float'),('img','Image')],string='Type')
    # int_max = fields.Integer(string='Max')
    # int_min = fields.Integer(string='Min')
    # float_min = fields.Float(string='Min')
    # float_min = fields.Float(string='Min')
