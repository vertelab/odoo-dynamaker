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
        
        
        # Look up sale order lines and compare to already created MRP production records and
        # compare the sale_line_id. 
        # If the id already exists then remove id and insert the next sale_order_line_id to mrp_procuction.sale_line_id
        sale_order = self.env['sale.order'].search([('name','=', vals['origin'])])
        line_ids = []
        if sale_order:
            lines = self.env['sale.order.line'].search([('order_id','=',sale_order.id)])
            if lines:
                for line in lines:
                    if line.product_template_id.dynamaker_product:
                        line_ids.append(line.id)
            
            mrp_production_ids = self.env['mrp.production'].search([('origin','=', sale_order.name)])
            if mrp_production_ids:
                for mrp_production in mrp_production_ids:
                    if mrp_production.sale_line_id.id in line_ids:
                        line_ids.remove(mrp_production.sale_line_id.id)
            if line_ids:
                vals.update({'sale_line_id': line_ids[0]})
                    

        res = super(MrpProduction, self).create(vals)
        res._get_sale_order_attachment_to_mrp(vals)
        return res

    def _get_sale_order_attachment_to_mrp(self, vals):
        origin_name = vals.get('origin')
        sale_order = self.env['sale.order'].search([('name','=',origin_name)])
        sale_order_line_ids = self.env['sale.order.line'].search([('order_id', '=', sale_order.id)])
        
        for line in sale_order_line_ids:
            sale_order_line_attachment = self.env['ir.attachment'].search([('res_id', '=', line.id),('res_model', '=', 'sale.order.line')])
            if sale_order_line_attachment:
                attachment = request.env['ir.attachment'].create({
                    'name': f'{origin_name}.pdf',
                    'res_model': 'mrp.production',
                    'type': sale_order_line_attachment.type,
                    'mimetype': sale_order_line_attachment.mimetype,
                    'store_fname': sale_order_line_attachment.store_fname,
                    'checksum': sale_order_line_attachment.checksum,
                    'file_size': sale_order_line_attachment.file_size,
                    'index_content': sale_order_line_attachment.index_content,
                    'res_id': self.id
                })
