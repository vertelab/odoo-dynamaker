# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)


class DynamakerProductAttribute(models.Model):
    _inherit = "product.attribute"

    display_type = fields.Selection(selection_add=[
        ('hidden_text', 'Hidden Text')])


class Product(models.Model):
    _inherit = 'product.template'

    dynamaker_price = fields.Float(compute='_dynamaker_price')

    def _dynamaker_price(self):
        line_id = self.env.context.get('order_line_id')
        custom_values = self.env.context.get('custom_values')
        line = None
        if line_id:
            line = self.env['sale.order.line'].sudo().browse(line_id)
        for product in self:
            if not (line or custom_values):
                product.dynamaker_price = product.list_price
                continue
            kw = {}
            if line_id:
                for custom_value in line.product_custom_attribute_value_ids:
                    try:
                        cleaned_value = float(custom_value.custom_value)
                    except Exception as err:
                        _logger.exception(err)
                        cleaned_value = custom_value.custom_value
                    kw[custom_value.custom_product_template_attribute_value_id.name] = cleaned_value # noqa:E501
            
            elif custom_values:
                for item in custom_values:
                    
                    try:
                        cleaned_value = float(item["custom_value"])
                    except Exception as err:
                        _logger.exception(err)
                        cleaned_value = item["custom_value"]
                    if cleaned_value:
                        kw[item["attribute_value_name"]] = cleaned_value
            price = DynamakerProductTemplate._compute_price(product, **kw)
            product.dynamaker_price = price


class DynamakerProductTemplate(models.Model):
    _inherit = "product.template"
    
    DEFAULT_PYTHON_CODE = """# Specify the python price algorithm.
#  - Access the product attributes through the 'kw' dict, eg. kw['width'], and kw['length'].
#  - Just set the price variable, e.g. price = kw['width'] * kw['length'].
#\n\n\n\n"""

    python_code = fields.Text('Price algorithm', default=DEFAULT_PYTHON_CODE,
        help="Write a Python algorithm that returns the price of the product.")

    dynamaker_product = fields.Boolean(string='Dynamaker Product', default=False) # noqa:E501

    dynamaker_url = fields.Char(string='Dynamaker URL', size=64, trim=True)

    def _compute_price(self, **kw):
        # construct input to price algorithm
        ldict = {'kw': kw}
        # safely execute user generated python code with input
        safe_eval(self.python_code.strip(), ldict, mode="exec", nocopy=True)
        return ldict['price']


class WebsiteProductConfiguratorDynamaker(http.Controller):
    @http.route(['/product_configurator/dynamaker_price'],
                type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self, **kw):
        qty = kw.get("qty", 1)
        product_id = int(kw.get('custom_values', {}).get("product_id"))
        custom_values = []
        for key, value in kw.get('custom_values', {}).items():
            custom_values.append({'attribute_value_name': key, 'custom_value': value})
        product = request.env['product.template'].browse(product_id)
        product = product.product_variant_ids[0].with_context(
            custom_values=custom_values)
        pricelist = request.website.get_current_pricelist()
        price = pricelist.get_product_price(product, qty, request.env.user.partner_id)
        price = round(price, pricelist.currency_id.decimal_places)
        return {'price': f"{price:.2f}"}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None,
                     add_qty=0, set_qty=0, **kwargs):
        self.ensure_one()
        product_context = dict(self.env.context)
        product_context.setdefault('lang', self.sudo().partner_id.lang)
        SaleOrderLineSudo = self.env['sale.order.line'].sudo().with_context(product_context) # noqa:E501
        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0
        order_line = False
        if self.state != 'draft':
            request.session['sale_order_id'] = None
            raise UserError(_('It is forbidden to modify a sales order which is not in draft status.')) # noqa:E501
        if line_id:
            order_line = self._cart_find_product_line(product_id,line_id, **kwargs)[:1]  # noqa:E501
            res = super(SaleOrder, self.with_context(order_line_id=order_line.id))._cart_update(product_id=product_id,  # noqa:E501
                        line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)  # noqa:E501
        else:
            res = super(SaleOrder, self.with_context(custom_values=kwargs.get('product_custom_attribute_values')
                        or []))._cart_update(product_id=product_id, line_id=line_id,
                        add_qty=add_qty, set_qty=set_qty, **kwargs)
        return res


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        # adds env.context to all dynamaker products in products_qty_partner
        # who have either an order_line_id or custom_values scraps dynamaker
        # products which dont have either of those two attributes.
        # This is because atleast one of these attributes are
        # necessary to calculate the price of a dynamaker_product
        pqp = []
        for product, qty, partner in products_qty_partner:
            if product.dynamaker_product and (self.env.context.get("order_line_id") or self.env.context.get("custom_values")):
                pqp.append((product.with_context(**self.env.context), qty, partner))
            else:
                pqp.append((product, qty, partner))
        products_qty_partner = pqp
        return super(Pricelist, self)._compute_price_rule(products_qty_partner,
            date=date, uom_id=uom_id)


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(selection_add=[
        ('dynamaker_price', 'Dynamaker price')],
        help='Base price for computation.\n'
         'Sales Price: The base price will be the Sales Price.\n'
         'Cost Price : The base price will be the cost price.\n'
         'Other Pricelist : Computation of the base price based on another Pricelist.'
         'Dynamaker pricelist : pricelist for custom products')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info(self, combination=False, product_id=False,add_qty=1,
        pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(combination=combination,
        product_id=product_id, add_qty=add_qty, pricelist=pricelist,
        parent_combination=parent_combination, only_template=only_template)

        product = self.env['product.product'].browse(combination_info['product_id']) or self
        combination_info.update(
            dynamaker_product=product[0]['dynamaker_product']
        )
        return combination_info
