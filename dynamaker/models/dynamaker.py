# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import base64

import logging
_logger = logging.getLogger(__name__)

    

class WebsiteProductDynamakerDrawing(http.Controller):
    @http.route(['/dynamaker/drawing'],
                type='json', auth='public', website=True)
    def product_configurator_dynamaker_price(self, **kw):
        blob = kw.get('blobFile')
        split_blob = blob.split(",")
        file_data = split_blob[1]
        file_header = split_blob[0]    
        file_name = 'tempfile.dfx'
        if file_header == 'data:application/pdf;base64':
            file_name = 'tempfile.pdf'
        attachment = request.env['ir.attachment'].create({
                'name': file_name,
                'res_model': 'sale.order.line',
                'datas': file_data,
            })
        
        return {'attachment_id': f"{attachment.id}"}
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # attachment_ids = fields.Many2many('ir.attachment', 'sale_order_line_drawing_ir_attachments_rel','rental_id', 'attachment_id', string="Attachments")
        
    # return res
