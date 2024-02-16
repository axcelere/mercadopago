# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_pos_mp = fields.Boolean(string="MP Payment Terminal",
                                        help="The transactions are processed by MP. Set your MP credentials on the related payment method.")


class PosStoreMP(models.Model):
    _name = 'pos.store.mp'

    name = fields.Char(string="Store")


class PosTerminalMP(models.Model):
    _name = 'pos.terminal.mp'
    _description = "Pos Terminal mp"

    external_pos_id = fields.Char(string="Pos externo")
    mp_terminal_id = fields.Char(string="Identificador de la terminal")
    mp_pos_id = fields.Char(string="Pos ID")
    mp_terminal_number = fields.Char(string="Número de terminal")
    mp_operating_mode = fields.Char(string="Modo de operación")
    store_terminal_id = fields.Many2one('pos.store.terminal.mp', string="Store terminal")


class PosStoreTerminalMP(models.Model):
    _name = 'pos.store.terminal.mp'

    store_id = fields.Many2one('pos.store.mp', string="Store")
    config_id = fields.Many2one('pos.config', string="Punto de venta")
    pos_mp_id = fields.Char(string="Punto de venta ID")
    terminal_line_ids = fields.One2many(
        "pos.terminal.mp",
        "store_terminal_id",
        string="Terminal Line",
    )

    def get_terminal(self):
        pass


class PosConfig(models.Model):
    _inherit = 'pos.config'
#
#     module_pos_payway = fields.Boolean(string="Payway Integrated Card Payments")
#     access_token = fields.Char(string="Access token", compute='_get_payway_token', store=True)
#     api_key = fields.Char(string="Api Key", compute='_get_payway_token', store=True)
    mp_terminal_id = fields.Many2one('pos.terminal.mp', string='MP Terminal')
#     settlement = fields.Boolean(string="Settlement", compute='_make_settlement', store=True)
#     payway_token_updating = fields.Datetime(string='Fecha del actualizacion del token')
#
#     def _pos_ui_models_to_load(self):
#         result = super()._pos_ui_models_to_load()
#         new_model = 'pos.order'
#         if new_model not in result:
#             result.append(new_model)
#         return result
#
#     @api.depends('session_ids', 'session_ids.state')
#     def _make_settlement(self):
#         for pos_config in self:
#             if pos_config.current_session_state == 'closing_control' and not pos_config.settlement:
#                 pos_payment_method_id = self.env['pos.payment.method'].search([('use_payment_terminal', '=', 'payway')], limit=1)
#                 if pos_payment_method_id.payway_test_mode:
#                     url = TEST_BASE_API_URL
#                 else:
#                     url = PROD_BASE_API_URL
#                 cuit_cuil = pos_payment_method_id.company_id.vat
#                 subnet_acquirer_id = pos_payment_method_id.pos_payway_config_id.payway_acquier_id
#                 terminal_id = pos_config.payway_terminal_id.payway_terminal_number
#                 print_receipt = True
#                 access_token = pos_config.access_token or ''
#                 headers = {'Authorization': 'Bearer ' + '' + access_token}
#                 url = url + '' + BASE_PATH_SETTLEMENTS + '?cuit_cuil=%s&subnet_acquirer_id=%s&terminal_id=%s&print_receipt=%s' % (cuit_cuil, subnet_acquirer_id,terminal_id,print_receipt)
#                 response = requests.request("POST", url, headers=headers)
#                 if response.status_code == 200:
#                     response = response.json()
#                     _logger.info('****************Making close*******************************')
#                     _logger.info(response)
#                 pos_config.settlement = True
#
#     @api.depends('session_ids', 'session_ids.state')
#     def _get_payway_token(self):
#         for pos_config in self:
#             if pos_config.current_session_state in ['opened']:
#                 pos_payment_method_id = self.env['pos.payment.method'].search([('use_payment_terminal', '=', 'payway')], limit=1)
#                 if pos_payment_method_id.payway_test_mode:
#                     url = TEST_BASE_API_URL
#                 else:
#                     url = PROD_BASE_API_URL
#                 url = url + '' + '/v1/oauth/accesstoken?grant_type=client_credentials'
#                 headers = {'Authorization': pos_payment_method_id.pos_payway_config_id.payway_secret_basic or ''}
#                 _logger.info('****************Making Logging to Payway*******************************')
#                 response = requests.request("GET", url, headers=headers)
#                 pos_config.payway_token_updating = fields.datetime.now()
#                 if response.status_code == 200:
#                     response = response.json()
#                     _logger.info('********************Token %s ********************************' % response['access_token'])
#                     pos_config.access_token = response['access_token']
#                     pos_config.api_key = response['apiKey']
#                     pos_config.payway_token_updating = fields.datetime.now()
#                     pos_config.settlement = False
