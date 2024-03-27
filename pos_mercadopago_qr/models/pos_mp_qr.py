# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api, _
import requests
import json
import uuid
_logger = logging.getLogger(__name__)


class PosMPConfigurationQr(models.Model):
    _name = 'pos_mp.configuration.qr'
    _description = 'Point of Sale Payway Configuration'

    name = fields.Char(string='Name', required=True)
    mp_qr_url = fields.Char(string='Url', required=True)
    user_id = fields.Char(string='Usuario')
    mp_access_token = fields.Char(string='Access token')
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)


class PoSPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    pos_mp_qr_config_id = fields.Many2one('pos_mp.configuration.qr', string='MP Credentials', help='The configuration of MP used for this journal')
    mp_qr_test_mode = fields.Boolean(help='Run transactions in the test environment.')

    def _get_payment_terminal_selection(self):
        return super(PoSPaymentMethod, self)._get_payment_terminal_selection() + [('mp_qr', 'MP QR')]

    @api.onchange('use_payment_terminal')
    def _onchange_use_payment_terminal(self):
        super(PoSPaymentMethod, self)._onchange_use_payment_terminal()
        if self.use_payment_terminal != 'mp_qr':
            self.pos_mp_config_id = False


class PosOrder(models.Model):
    _inherit = "pos.order"

    mp_qr_payment_token = fields.Char(string='Payment token')

    def create_logs(self, config_id, action, headers, endpoint, status_code, payload, response):
        self.env['mp.log.qr'].create({
            'config_id': config_id.id,
            'action': action,
            'header': headers,
            'endpoint': endpoint,
            'status_code': status_code,
            'request': payload,
            'response': response,
        })
        self.env.cr.commit()

    def make_payment_mp_qr(self, order):
        pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
        sale_point_id = pos_session_id.config_id.sale_point_id
        pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
        configuration_id = pos_payment_method_id.pos_mp_qr_config_id
        user = configuration_id.user_id or ''
        access_token = configuration_id.mp_access_token or ''
        url = configuration_id.mp_qr_url
        endpoint = url + '' + 'instore/qr/seller/collectors/' + '' + user + '/stores/' + sale_point_id.store_box_id.external_store_id + '/pos/' + sale_point_id.external_id + '/orders'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
        items = []
        vals_product = {
                "id": sale_point_id.box_id,
                "title": 'Productos Varios',
                "currency_id": "ARS",
                "unit_price": order['amount_total'],
                "total_amount": order['amount_total'],
                "quantity": 1,
                "unit_measure": "unit",
                "description": 'Productos Varios',
        }
        items.append(vals_product)
        payload = {
            "external_reference": order['order_uid'],
            "description": order['order_name'],
            "items": items,
            "title": "Productos Varios",
            "total_amount": order['amount_total'],
        }
        _logger.info('*************************Sending  request to Payway for sale******************************')
        _logger.info('********************Payload ************************************************* %s' % payload)
        response = requests.request("PUT", endpoint, headers=headers, data=json.dumps(payload))
        if response.status_code == 204:
            payment_id = order['order_uid']
            _logger.info('****************Payment data %s ****************' % payment_id)
            vals = {
                'status_code': 200,
                'payment_id': payment_id
            }
        else:
            vals = {
                'status_code': response.status_code,
                'error': response.json()['message']
            }
        self.create_logs(pos_session_id.config_id, 'create_order', headers, endpoint, response.status_code, payload, '')
        return vals

    def updating_order(self, order):
        pos_order_id = self.env['pos.order'].search([('access_token', '=', order['access_token_order'])])
        pos_order_id.write({'mp_qr_payment_token': order['mp_qr_payment_id']})
        return True

    def make_cancel_mp(self, order):
        pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
        sale_point_id = pos_session_id.config_id.sale_point_id
        pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
        configuration_id = pos_payment_method_id.pos_mp_qr_config_id
        user = configuration_id.user_id or ''
        access_token = configuration_id.mp_access_token or ''
        url = configuration_id.mp_qr_url
        endpoint = url + '' + 'instore/qr/seller/collectors/' + '' + user + '/pos/' + sale_point_id.external_id + '/orders'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
        _logger.info('*************************Sending  request to MP for sale******************************')
        response = requests.request("DELETE", endpoint, headers=headers)
        if response.status_code == 204:
            _logger.info('**********************Payment info cancellations **************************')
            _logger.info(response)
        self.create_logs(pos_session_id.config_id, 'remove_order', headers, endpoint, response.status_code, '', '')

    def get_payment_status_mp(self, order):
        vals = {}
        pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
        pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
        configuration_id = pos_payment_method_id.pos_mp_qr_config_id
        access_token = configuration_id.mp_access_token or ''
        url = configuration_id.mp_qr_url
        endpoint = url + '' + 'v1/payments/search?external_reference=' + '' + order['order_uid']
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
        _logger.info('*************************Sending  request to MPQR for sale******************************')
        response = requests.request("GET", endpoint, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            response = response.json()
            status = response['results'][-1]['status']
            vals = {
                'status_code': 200,
                'payment_status': status,
                'payment_id': response['results'][0]['id']
            }
        self.create_logs(pos_session_id.config_id, 'get_order', headers, endpoint, status_code, '', response)
        return vals

    def make_refunds_mp(self, order):
        pos_order_id = self.env['pos.order'].search([('id', 'in', order['toRefundLines_ids'])])
        pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
        configuration_id = pos_payment_method_id.pos_mp_qr_config_id
        access_token = configuration_id.mp_access_token or ''
        url = configuration_id.mp_qr_url
        idempotency = str(uuid.uuid4())
        endpoint = url + '' + 'v1/payments/' + '' + pos_order_id.mp_qr_payment_token + '/refunds'
        headers = {'Content-Type': 'application/json', 'X-Idempotency-Key': idempotency,  'Authorization': 'Bearer ' + '' + access_token}
        _logger.info('*************************Sending  request to MPQR for sale******************************')
        payload = {
            'amount': abs(order['amount_total'])
        }
        response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
        status_code = response.status_code
        if status_code == 204:
            response = response.json()
            payment_id = response
        else:
            response = response.json()
            vals = {
                'error': response['error'],
                'message': response['message']
            }
        self.create_logs(pos_order_id.config_id, 'refund_order', headers, endpoint, status_code, payload, response)
        return vals









