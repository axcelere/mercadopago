# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class PosMPConfiguration(models.Model):
    _name = 'pos_mp.configuration'
    _description = 'Point of Sale Payway Configuration'

    name = fields.Char(string='Name', required=True)
    mp_access_token = fields.Char(string='Access token')
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)


class PoSPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    pos_mp_config_id = fields.Many2one('pos_mp.configuration', string='MP Credentials', help='The configuration of MP used for this journal')
    mp_test_mode = fields.Boolean(help='Run transactions in the test environment.')

    def _get_payment_terminal_selection(self):
        return super(PoSPaymentMethod, self)._get_payment_terminal_selection() + [('mp', 'MP')]

    @api.onchange('use_payment_terminal')
    def _onchange_use_payment_terminal(self):
        super(PoSPaymentMethod, self)._onchange_use_payment_terminal()
        if self.use_payment_terminal != 'mp':
            self.pos_mp_config_id = False


class PosOrder(models.Model):
    _inherit = "pos.order"
#
    mp_payment_token = fields.Char(string='Payment token')
#
    def make_payment_mp(self, order):
        # financial_surcharge = 0.0
        # pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
        # installment_id = self.env['account.card.installment'].search([('id', '=', order['installment'])])
        # if installment_id:
        #     financial_surcharge = installment_id.financial_surcharge
        # current_date = fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # current_date = datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
        # payway_token_updating = pos_session_id.config_id.payway_token_updating.strftime('%Y-%m-%d %H:%M:%S')
        # payway_token_updating = datetime.strptime(payway_token_updating, '%Y-%m-%d %H:%M:%S')
        #
        # diff_time = abs((payway_token_updating - current_date).total_seconds() / 3600)
        # if diff_time >= 1:
        #     pos_session_id.config_id._get_payway_token()
        # pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
        # if pos_payment_method_id.payway_test_mode:
        #     url = TEST_BASE_API_URL
        # else:
        #     url = PROD_BASE_API_URL
        # access_token = pos_session_id.config_id.access_token or ''
        # cuit_cuil = pos_payment_method_id.company_id.vat
        # endpoint = url + '' + BASE_PATH_PAYMENT + '' + '/payments?cuit_cuil=' + '' + cuit_cuil
        # subnet_acquirer_id = pos_payment_method_id.pos_payway_config_id.payway_acquier_id
        # headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
        # if isinstance(order['amount_total'], int):
        #     amount_total = str(order['amount_total']) + '00'
        # else:
        #     amount_total = round(order['amount_total'], 2)
        #     amount_total = (financial_surcharge * amount_total) + amount_total
        #     amount_total_str = str(amount_total).split(".")[0] + str(amount_total).split(".")[1]
        # payload = {
        #     "payment_request_data": {
        #         "subnet_acquirer_id": subnet_acquirer_id,
        #         "payment_amount": amount_total_str,
        #         "terminal_menu_text": "Pedido de" + ' $' + str(amount_total),
        #         "ecr_provider": pos_payment_method_id.company_id.name,
        #         "ecr_name": pos_payment_method_id.company_id.name,
        #         "ecr_version": "1.0",
        #         "change_amount": "0",
        #         "ecr_transaction_id": None,
        #         "installments_number": int(installment_id.installment) if installment_id else 1,
        #         "bank_account_type": None,
        #         "payment_plan_id": None,
        #         "print_method": "MOBITEF_NON_FISCAL",
        #         "print_copies": "BOTH",
        #         "terminals_list": [{"terminal_id": pos_session_id.config_id.payway_terminal_id.payway_terminal_number}],
        #         "card_brand_product": None,
        #         "terminal_operation_method": "CARD",
        #         "qr_benefit_code": None,
        #         "trx_receipt_notes": None,
        #         "card_holder_id": None
        #     }
        # }
        # _logger.info('*************************Sending  request to Payway for sale******************************')
        # _logger.info('********************Payload ************************************************* %s' % payload)
        # response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
        # _logger.info('**********************Payment response %s **************************' % response)
        # if response.status_code == 200:
        #     response = response.json()
        #     payment_id = response['payment_data']['payment_id']
        #     _logger.info('**********************Payment data %s **************************' % response['payment_data'])
        #     vals = {
        #         'status_code': 200,
        #         'access_token': payment_id
        #     }
        # else:
        #     vals = {
        #         'status_code': response.status_code,
        #         'error': response.json()['errors'][0]['title']
        #     }
        vals = {}
        return vals
#
#     def make_cancel(self, order):
#         pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
#         current_date = fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         current_date = datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
#         payway_token_updating = pos_session_id.config_id.payway_token_updating.strftime('%Y-%m-%d %H:%M:%S')
#         payway_token_updating = datetime.strptime(payway_token_updating, '%Y-%m-%d %H:%M:%S')
#         diff_time = abs((payway_token_updating - current_date).total_seconds() / 3600)
#         if diff_time >= 1:
#             pos_session_id.config_id._get_payway_token()
#
#         pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
#         if pos_payment_method_id.payway_test_mode:
#             url = TEST_BASE_API_URL
#         else:
#             url = PROD_BASE_API_URL
#         access_token = pos_session_id.config_id.access_token or ''
#         cuit_cuil = pos_payment_method_id.company_id.vat
#         subnet_acquirer_id = pos_payment_method_id.pos_payway_config_id.payway_acquier_id
#
#         headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
#
#         payment_type_build = order['payment_type_build']
#         if payment_type_build == 'reversals_refunds':
#             payments = order["access_token_payment"]
#             if pos_payment_method_id.card_brand == 'AMEX':
#                 recurse = BASE_PATH_REFUNDS
#                 payment_type_build = 'refunds'
#             else:
#                 recurse = BASE_PATH_REVERSAL
#                 payment_type_build = 'reversals'
#         else:
#             recurse = BASE_PATH_PAYMENT
#             payments = order["access_token_payment"]
#
#         endpoint = url + '' + recurse + '' + '/' + payment_type_build +'/'+ payments + '/cancellations' +'?cuit_cuil=' + '' + cuit_cuil +'&subnet_acquirer_id=' + '' + subnet_acquirer_id
#         _logger.info('******************** Endpoint ************************************************* %s' % endpoint)
#         response = requests.request("PUT", endpoint, headers=headers)
#         if response.status_code == 200:
#             response = response.json()
#             _logger.info('**********************Payment info cancellations **************************')
#             _logger.info(response)
#
#     def updating_order(self, order):
#         pos_order_id = self.env['pos.order'].search([('access_token', '=', order['access_token_order'])])
#         pos_order_id.write({'payway_payment_token': order['access_token_payment']})
#         return True
#
#     def get_payment_status(self, order):
#         pos_session_id = self.env['pos.session'].search([('id', '=', order['pos_session_id'])])
#         current_date = fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         current_date = datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
#         payway_token_updating = pos_session_id.config_id.payway_token_updating.strftime('%Y-%m-%d %H:%M:%S')
#         payway_token_updating = datetime.strptime(payway_token_updating, '%Y-%m-%d %H:%M:%S')
#         diff_time = abs((payway_token_updating - current_date).total_seconds() / 3600)
#         if diff_time >= 1:
#             pos_session_id.config_id._get_payway_token()
#         pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', order['payment_method_id'])])
#         if pos_payment_method_id.payway_test_mode:
#             url = TEST_BASE_API_URL
#         else:
#             url = PROD_BASE_API_URL
#         access_token = pos_session_id.config_id.access_token or ''
#         cuit_cuil = pos_payment_method_id.company_id.vat
#         subnet_acquirer_id = pos_payment_method_id.pos_payway_config_id.payway_acquier_id
#         payments = order["access_token_payment"]
#         headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
#
#         payment_type_build = order['payment_type_build']
#         if payment_type_build == 'reversals_refunds':
#             if pos_payment_method_id.card_brand == 'AMEX':
#                 recurse = BASE_PATH_REFUNDS
#                 payment_type_build = 'refunds'
#             else:
#                 recurse = BASE_PATH_REVERSAL
#                 payment_type_build = 'reversals'
#         else:
#             recurse = BASE_PATH_PAYMENT
#         endpoint = url + '' + recurse + '' + '/' + payment_type_build +'/'+ payments + '?cuit_cuil=' + '' + cuit_cuil +'&subnet_acquirer_id=' + '' + subnet_acquirer_id
#         _logger.info('*************************GET STATUS URL******************************')
#         _logger.info(endpoint)
#         response = requests.request("GET", endpoint, headers=headers)
#         if response.status_code == 200:
#             response = response.json()
#             _logger.info('*************************GET STATUS******************************')
#             _logger.info(response)
#             if payment_type_build == 'reversals':
#                 if response['reversal_data']['reversal_status']:
#                     vals = {
#                         'status_code': 200,
#                         'payment_status': response['reversal_data']['reversal_status']
#                     }
#             if payment_type_build == 'payments':
#                 if response['payment_data']['payment_status']:
#                     vals = {
#                         'status_code': 200,
#                         'payment_status': response['payment_data']['payment_status']
#                     }
#             if payment_type_build == 'refunds':
#                 if response['refund_data']['refund_status']:
#                     vals = {
#                         'status_code': 200,
#                         'payment_status': response['refund_data']['refund_status']
#                     }
#         else:
#             vals = {
#                 'status_code': response.status_code,
#                 'error': response.json()['errors'][0]['title']
#             }
#             # vals = {
#             #     'status_code': 200,
#             #     'payment_status': 'CONFIRMED'
#             # }
#         return vals
#
#     def make_refunds(self, orders):
#         pos_session_id = self.env['pos.session'].search([('id', '=', orders['pos_session_id'])])
#         pos_order_id = self.env['pos.order'].search([('id', 'in', orders['toRefundLines_ids'])])
#         current_date = fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         current_date = datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
#         payway_token_updating = pos_session_id.config_id.payway_token_updating.strftime('%Y-%m-%d %H:%M:%S')
#         payway_token_updating = datetime.strptime(payway_token_updating, '%Y-%m-%d %H:%M:%S')
#         diff_time = abs((payway_token_updating - current_date).total_seconds() / 3600)
#         if diff_time >= 1:
#             pos_session_id.config_id._get_payway_token()
#         pos_payment_method_id = self.env['pos.payment.method'].search([('id', '=', orders['payment_method_id'])])
#         if pos_payment_method_id.payway_test_mode:
#             url = TEST_BASE_API_URL
#         else:
#             url = PROD_BASE_API_URL
#         access_token = pos_session_id.config_id.access_token or ''
#         subnet_acquirer_id = pos_payment_method_id.pos_payway_config_id.payway_acquier_id
#         cuit_cuil = pos_payment_method_id.company_id.vat
#         headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + '' + access_token}
#         amount_return = round(abs(float(orders['amount_total'])), 2)
#         if isinstance(orders['amount_total'], int):
#             amount_total = str(abs(orders['amount_total'])) + '00'
#         else:
#             amount_total = round(abs(orders['amount_total']), 2)
#             amount_total_str = str(amount_total).split(".")[0] + str(amount_total).split(".")[1]
#         if pos_payment_method_id.card_brand == 'AMEX':
#             endpoint = url + '' + BASE_PATH_REFUNDS + '' + '/refunds?cuit_cuil=' + '' + cuit_cuil
#             payload = {
#                 "subnet_acquirer_id": subnet_acquirer_id,
#                 "refund_amount": amount_total_str,
#                 "terminal_menu_text": "Devolución NR" + ' $' + str(amount_total),
#                 "ecr_provider": pos_payment_method_id.company_id.name,
#                 "ecr_name": pos_payment_method_id.company_id.name,
#                 "ecr_version": "1.0",
#                 "ecr_transaction_id": None,
#                 "print_copies": "BOTH",
#                 "terminals_list": [{"terminal_id": pos_session_id.config_id.payway_terminal_id.payway_terminal_number}],
#                 "card_brand_product": None
#             }
#             response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
#             if response.status_code == 200:
#                 response = response.json()
#                 _logger.info('*************************Making Refund******************************')
#                 _logger.info(response)
#                 refund_id = response['refund_data']['refund_id']
#                 vals = {
#                     'status_code': 200,
#                     'access_token': refund_id
#                 }
#             else:
#                 vals = {
#                     'status_code': response.status_code,
#                     'error': response.json()['errors'][0]['title']
#                 }
#             return vals
#         else:
#             endpoint = url + '' + BASE_PATH_REVERSAL + '' + '/reversals?cuit_cuil=' + '' + cuit_cuil
#             payload = {
#                 "reversal_request_data": {
#                     "subnet_acquirer_id": subnet_acquirer_id,
#                     "payment_id": pos_order_id[0].payway_payment_token,
#                     "terminal_menu_text": "Pedido de" + ' $' + str(amount_return),
#                     "ecr_transaction_id": None,
#                     "print_copies": 2,
#                     "terminals_list": [
#                         {"terminal_id": pos_session_id.config_id.payway_terminal_id.payway_terminal_number}],
#                 }
#             }
#             response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
#             if response.status_code == 200:
#                 response = response.json()
#                 _logger.info('*************************Making Reversal******************************')
#                 _logger.info(response)
#                 payment_id = response['reversal_data']['payment_id']
#                 vals = {
#                     'status_code': 200,
#                     'access_token': payment_id
#                 }
#             else:
#                 vals = {
#                     'status_code': response.status_code,
#                     'error': response.json()['errors'][0]['title']
#                 }
#             return vals






