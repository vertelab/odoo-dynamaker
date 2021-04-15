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
        splitBlob = blob.split(",")
        fileData = splitBlob[1]
        fileHeader = splitBlob[0]    

        attachment = request.env['ir.attachment'].create({
            'name': 'testfil.pdf',
            'res_model': 'sale.order',
            'datas': fileData,
        })
        return {'attachment_id': f"{attachment.id}"}
