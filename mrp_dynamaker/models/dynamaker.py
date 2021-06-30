# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, tools, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
import base64

import logging
_logger = logging.getLogger(__name__)



class DynamakerMrp(models.Model):
    _name = 'dynamaker.mrp'



class WebsiteProductDynamakerDrawing(http.Controller):
    @http.route(['/dynamaker/mrpdata'],
                type='json', auth='public', website=True)
    def parse_dynamaker_mrp_data(self, **kw):
        data = kw.get('mrpData')
        _logger.info(f'david data: {data}')
        _logger.info(f'david drawings: {data.get("drawings")}')
        _logger.info(f'david quantity: {data.get("quantities")}')
        drawings = data.get("drawings")
        if not drawings:
            return
        attachment_ids = []
        for drawing in drawings:
            key, value = list(drawing.items())[0]
            drawing_blob = value.split(",")
            file_data = drawing_blob[1]
            file_header = drawing_blob[0]

            suffix = "pdf" \
                if file_header == "data:application/pdf;base64" \
                else "dtx"
            file_name = f'{key}.{suffix}'
            _logger.info(f'david attachment name so: {file_name}')
            attachment = request.env['ir.attachment'].create({
                    'name': file_name,
                    'res_model': 'sale.order.line',
                    'datas': file_data,
                })
            attachment_ids.append(attachment.id)
        _logger.info(f'drawings attachment ids: {attachment_ids}')
        return {'attachment_id': f"{attachment_ids}"}
