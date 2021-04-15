# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    
    @api.model
    def create(self, vals):
        res = super(MrpProduction, self).create(vals)
        res._get_sale_order_attachment_to_mrp(vals)
        return res

    def _get_sale_order_attachment_to_mrp(self, vals):
        origin_name = vals.get('origin')
        origin_obj = self.env['sale.order'].search([('name','=',origin_name)])
        if origin_obj:
            sale_order_attachment = self.env['ir.attachment'].search([('res_id','=',origin_obj.id)])
            if sale_order_attachment:
                attachment = request.env['ir.attachment'].create({
                    'name': f'{origin_name}.pdf',
                    'res_model': 'mrp.production',
                    'type': sale_order_attachment.type,
                    'mimetype': sale_order_attachment.mimetype,
                    'store_fname': sale_order_attachment.store_fname,
                    'checksum': sale_order_attachment.checksum,
                    'file_size': sale_order_attachment.file_size,
                    'index_content': sale_order_attachment.index_content,
                    'res_id': self.id
                })
