# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from collections import namedtuple, OrderedDict, defaultdict
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_line_id = fields.Many2one(
        'sale.order.line', 'Sale Order Line',
        readonly=True,)

    @api.model
    def create(self, vals):

        # # TODO: Avoid searching on origin

        # Get sale order lines that are Dynamaker products, and that are not present in mrp production already.
        # Then update vals to set sale order line to created mrp.production record.
        sale_order = self.env['sale.order'].search([('name', '=', vals['origin'])])
        mrp_production_ids = self.env['mrp.production'].search([('origin', '=', sale_order.name)])
        line_ids = sale_order.order_line.with_context(
                m_line=mrp_production_ids).filtered(
                        lambda l: l.product_template_id.dynamaker_product and not
                        l.id in l._context['m_line'].mapped('sale_line_id.id')).ids
        if line_ids:
            vals.update({'sale_line_id': line_ids[0]})


        res = super(MrpProduction, self).create(vals)


        # Create a copy of bom list
        # Then loop over and set new vals to bom line ids
        # Set bom to new one with updated bom line vals
        if res.product_id.dynamaker_product:
            res._get_sale_order_attachment_to_mrp(vals)
            bom_copy = res.bom_id.copy()
            bom_copy.code = sale_order.name
            for bom_line in bom_copy.bom_line_ids:
                sale_lines = self.env['sale.order.line'].browse(line_ids)
                for sale_line in sale_lines:
                    for custom_attr in sale_line.product_custom_attribute_value_ids:
                        try:
                            if custom_attr.name.split(':')[1].strip() == bom_line.product_id.default_code:
                                bom_line.product_qty = int(custom_attr.custom_value)
                        except Exception as e:
                            _logger.warning(f'Attribute not found, {e}')


            res.bom_id = bom_copy

        return res

    def _get_sale_order_attachment_to_mrp(self, vals):

        # Getting the attachment from sale_line_id and creating a
        # new attachment for mrp_production

        sale_order_line_attachment = self.env['ir.attachment'].search([
                                    ('res_id', '=', vals.get('sale_line_id')),
                                    ('res_model', '=', 'sale.order.line')
                                    ])
        if sale_order_line_attachment:
            for line in sale_order_line_attachment:
                attachment = request.env['ir.attachment'].create({
                    'name': '{}-{}'.format(vals.get('origin'), line.name),
                    'res_model': 'mrp.production',
                    'type': line.type,
                    'mimetype': line.mimetype,
                    'store_fname': line.store_fname,
                    'checksum': line.checksum,
                    'file_size': line.file_size,
                    'index_content': line.index_content,
                    'res_id': self.id
                })
