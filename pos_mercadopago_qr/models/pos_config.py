# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import logging
_logger = logging.getLogger(__name__)

WEEKDAY_SELECTION = [
    ('MON', 'Lun'),
    ('TUE', 'Mar'),
    ('WED', 'Mié'),
    ('THU', 'Jue'),
    ('FRI', 'Vie'),
    ('SAT', 'Sáb'),
    ('SUN', 'Dom'),
]

RRULE_TYPE_SELECTION = [
    ('daily', 'Days'),
    ('weekly', 'Weeks'),
    ('monthly', 'Months'),
    ('yearly', 'Years'),
]

def _get_select_time(self):
    select_list_time = [('01:00', '01:00'), ('01:30', '01:30'), ('02:00', '02:00'), ('02:30', '02:30'),
                        ('03:00', '03:00'), ('03:30', '03:30'), ('04:00', '04:00'), ('04:30', '04:30'),
                        ('05:00', '05:00'), ('05:30', '05:30'), ('06:00', '06:00'), ('06:30', '06:30'),
                        ('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'),
                        ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'),
                        ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'),
                        ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'),
                        ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'),
                        ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'),
                        ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
                        ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'),
                        ('23:00', '23:00'), ('23:30', '23:30'), ('23:59', '23:59'), ('00:00', '00:00'), ('00:30', '00:30'),
                        ]
    return select_list_time


def _get_select_time_close(self):
    select_list_time = [('01:00', '01:00'), ('01:30', '01:30'), ('02:00', '02:00'), ('02:30', '02:30'),
                        ('03:00', '03:00'), ('03:30', '03:30'), ('04:00', '04:00'), ('04:30', '04:30'),
                        ('05:00', '05:00'), ('05:30', '05:30'), ('06:00', '06:00'), ('06:30', '06:30'),
                        ('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'),
                        ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'),
                        ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'),
                        ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'),
                        ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'),
                        ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'),
                        ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
                        ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'),
                        ('23:00', '23:00'), ('23:30', '23:30'), ('23:59', '23:59'), ('00:00', '00:00'), ('00:30', '00:30'),
                        ]
    return select_list_time


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_pos_mp_qr = fields.Boolean(string="MP Payment Terminal QR",
                                        help="The transactions are processed by MP. Set your MP credentials on the related payment method.")


class PosStoreMPQr(models.Model):
    _name = 'pos.store.mp.qr'

    name = fields.Char(string="Store")
    external_id = fields.Char(string="Store", store=True)
    street_number = fields.Char(string="Número de calle")
    street_name = fields.Char(string="Nombre de calle")
    city_name = fields.Char(string="Ciudad")
    state_id = fields.Many2one('res.country.state', string="Provincia")
    latitude = fields.Float('Geo Latitude', digits=(10, 7))
    longitude = fields.Float('Geo Longitude', digits=(10, 7))
    ref = fields.Char(string="Referencia")
    external_store_id = fields.Char(string="Store ID")
    address_id = fields.Char(string="Address ID")

    mon = fields.Boolean(string='Lunes')
    tue = fields.Boolean()
    wed = fields.Boolean()
    thu = fields.Boolean()
    fri = fields.Boolean()
    sat = fields.Boolean()
    sun = fields.Boolean()
    weekday = fields.Selection(WEEKDAY_SELECTION, string='Weekday')
    interval = fields.Integer(default=1)
    rrule_type = fields.Selection(RRULE_TYPE_SELECTION, default='weekly')
    active_range = fields.Boolean(string='Active Range', default=False)
    h24 = fields.Boolean(string='24H', default=False)
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('publish', 'Publicado')
        ],
        string='Estado', default='draft'
    )

    # Monday
    open_time_mon = fields.Selection(selection=_get_select_time, strint='Abre', store=True)
    close_time_mon = fields.Selection(selection=_get_select_time_close, strint='Cierra', store=True)

    # Tuesday
    open_time_tue = fields.Selection(selection=_get_select_time, store=True)
    close_time_tue = fields.Selection(selection=_get_select_time_close, store=True)

    # Wednesday
    open_time_wed = fields.Selection(selection=_get_select_time, store=True)
    close_time_wed = fields.Selection(selection=_get_select_time_close, store=True)

    # Thursday
    open_time_thu = fields.Selection(selection=_get_select_time, store=True)
    close_time_thu = fields.Selection(selection=_get_select_time_close, store=True)

    # Friday
    open_time_fir = fields.Selection(selection=_get_select_time, store=True)
    close_time_fir = fields.Selection(selection=_get_select_time_close, store=True)

    # Saturday
    open_time_sat = fields.Selection(selection=_get_select_time, store=True)
    close_time_sat = fields.Selection(selection=_get_select_time_close, store=True)

    # Sunday
    open_time_sun = fields.Selection(selection=_get_select_time, store=True)
    close_time_sun = fields.Selection(selection=_get_select_time_close, store=True)

    def get_business_hours(self):
        vals = {}
        for rec in self:
            if rec.mon:
                vals["monday"] = [{"open": rec.open_time_mon, "close": rec.close_time_mon}]
            if rec.tue:
                vals["tuesday"] = [{"open": rec.open_time_tue, "close": rec.close_time_tue}]
            if rec.wed:
                vals["wednesday"] = [{"open": rec.open_time_wed, "close": rec.close_time_wed}]
            if rec.thu:
                vals["thursday"] = [{"open": rec.open_time_thu, "close": rec.close_time_thu}]
            if rec.fri:
                vals["friday"] = [{"open": rec.open_time_fir, "close": rec.close_time_fir}]
            if rec.sat:
                vals["saturday"] = [{"open": rec.open_time_sat, "close": rec.close_time_sat}]
            if rec.sun:
                vals["sunday"] = [{"open": rec.open_time_sun, "close": rec.close_time_sun}]
        return vals

    def publish_branch(self):
        credential_id = self.env['pos_mp.configuration.qr'].search([])
        user = credential_id.user_id
        url = credential_id.mp_qr_url + 'users/' + user + '/stores'
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + '' + credential_id.mp_access_token,
        }
        payload = {
              "business_hours": self.get_business_hours(),
              "external_id": self.external_id,
              "location": {
                "street_number": self.street_number,
                "street_name": self.street_name,
                "city_name": self.city_name,
                "state_name": self.state_id.name,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "reference": self.ref
              },
              "name": self.name
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
        except ConnectionError as error:
            raise ValidationError('Error comunicandose con la plataforma. Respuesta con error %s' % error)
        if response.status_code == 201:
            data_to_json = response.json()
            self.write({'state': 'publish', 'external_store_id': data_to_json['id'], 'address_id': data_to_json['location']['id']})
        else:
            data_to_json = response.json()
            raise ValidationError('Error: %s' % data_to_json)

    def update_branch(self):
        credential_id = self.env['pos_mp.configuration.qr'].search([])
        user = credential_id.user_id
        url = credential_id.mp_qr_url + 'users/' + user + '/stores/' + self.external_store_id
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + '' + credential_id.mp_access_token,
        }
        payload = {
            "business_hours": self.get_business_hours(),
            "external_id": self.external_id,
            "location": {
                "street_number": self.street_number,
                "street_name": self.street_name,
                "city_name": self.city_name,
                "state_name": self.state_id.name,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "reference": self.ref
            },
            "name": self.name
        }
        try:
            response = requests.put(url, headers=headers, json=payload)
        except ConnectionError as error:
            raise ValidationError('Error comunicandose con la plataforma. Respuesta con error %s' % error)
        if response.status_code == 200:
            data_to_json = response.json()
            self.write({'state': 'publish', 'external_store_id': data_to_json['id'], 'address_id': data_to_json['location']['id']})
        else:
            data_to_json = response.json()
            raise ValidationError('Error: %s' % data_to_json)


class PosTerminalMPQr(models.Model):
    _name = 'pos.box.mp.qr'
    _description = "Pos Terminal mp qr"

    config_id = fields.Many2one('pos.config', string="Punto de venta")
    name = fields.Char(string="Nombre de la caja", related='config_id.name', store=True)
    category = fields.Selection(
        [
            ('621102', 'Argentina')
        ],
        string='Código MCC', default='621102')
    external_id = fields.Char(string="Identificador único de la caja")
    store_box_id = fields.Many2one('pos.store.box.mp.qr', string="Store terminal")
    image_qr = fields.Char(string="Image QR")
    template_document_qr = fields.Char(string="Template document QR")
    template_image_qr = fields.Char(string="Template image QR")
    qr_code = fields.Char(string="QR code")
    fixed_amount = fields.Boolean(string="Fixed amount")
    box_id = fields.Char(string="Box ID")
    store_id = fields.Char(string="Store")
    external_store_id = fields.Char(string="External Store")
    user_id = fields.Char(string="User")
    active_box = fields.Boolean(string="Estado")

    def remove_point_box(self):
        credential_id = self.env['pos_mp.configuration.qr'].search([])
        if self.box_id:
            url = credential_id.mp_qr_url + 'pos/' + self.box_id
            headers = {
                "Content-Type": "application/json",
                'Authorization': 'Bearer ' + '' + credential_id.mp_access_token,
            }
            try:
                response = requests.delete(url, headers=headers)
            except ConnectionError as error:
                raise ValidationError('Error comunicandose con la plataforma. Respuesta con error %s' % error)
            if response.status_code == 204:
                self.unlink()
            else:
                data_to_json = response.json()
                raise ValidationError('Error: %s' % data_to_json)
        else:
            self.unlink()

    def edit_point_box(self):
        credential_id = self.env['pos_mp.configuration.qr'].search([])
        url = credential_id.mp_qr_url + 'pos/' + self.box_id
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + '' + credential_id.mp_access_token,
        }
        for rec in self:
            payload = {
                "category": int(rec.category),
                "fixed_amount": rec.fixed_amount,
                "name": rec.name,
                "store_id": int(rec.store_box_id.store_id.external_store_id)
            }
            try:
                response = requests.put(url, headers=headers, json=payload)
            except ConnectionError as error:
                raise ValidationError('Error comunicandose con la plataforma. Respuesta con error %s' % error)
            if response.status_code == 200:
                data_to_json = response.json()
                rec.write({'image_qr': data_to_json['qr']['image'],
                           'template_document_qr': data_to_json['qr']['template_document'],
                           'template_image_qr': data_to_json['qr']['template_image'],
                           'qr_code': data_to_json['qr_code'],
                           'box_id': data_to_json['id'],
                           'active_box': True
                           })
            else:
                data_to_json = response.json()
                raise ValidationError('Error: %s' % data_to_json)


class PosStoreTerminalMPQr(models.Model):
    _name = 'pos.store.box.mp.qr'

    name = fields.Char(string="Punto de venta ID")
    store_id = fields.Many2one('pos.store.mp.qr', string="Store")
    external_store_id = fields.Char(string="Identificador del store", related='store_id.external_store_id')
    box_line_ids = fields.One2many(
        "pos.box.mp.qr",
        "store_box_id",
        string="Terminal Line",
    )
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('publish', 'Publicado')
        ],
        string='Estado', default='draft'
    )

    def publish_box(self):
        credential_id = self.env['pos_mp.configuration.qr'].search([])
        url = credential_id.mp_qr_url + 'pos'
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + '' + credential_id.mp_access_token,
        }
        for rec in self:
            for box in rec.box_line_ids.filtered(lambda x: not x.active_box):
                payload = {
                      "category": int(box.category),
                      "external_id": rec.store_id.external_id + '' + 'POS' + str(box.config_id.id) + str(box.id),
                      "external_store_id": rec.store_id.external_id,
                      "fixed_amount": box.fixed_amount,
                      "name": box.name,
                      "store_id": int(rec.store_id.external_store_id)
                }
                try:
                    response = requests.post(url, headers=headers, json=payload)
                except ConnectionError as error:
                    raise ValidationError('Error comunicandose con la plataforma. Respuesta con error %s' % error)
                if response.status_code == 201:
                    data_to_json = response.json()
                    box.write({'image_qr': data_to_json['qr']['image'],
                               'template_document_qr': data_to_json['qr']['template_document'],
                               'template_image_qr': data_to_json['qr']['template_image'],
                               'qr_code': data_to_json['qr_code'],
                               'box_id': data_to_json['id'],
                               'active_box': True,
                               'external_id': data_to_json['external_id'],
                               'store_id': data_to_json['store_id'],
                               'user_id': data_to_json['user_id'],
                               'external_store_id': data_to_json['external_store_id']})
                else:
                    data_to_json = response.json()
                    raise ValidationError('Error: %s' % data_to_json)
            box_active = len(rec.box_line_ids.filtered(lambda x: x.active_box))
            box = len(rec.box_line_ids)
            if box_active == box:
                rec.write({'state': 'publish'})

    def to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sale_point_id = fields.Many2one('pos.box.mp.qr', string='Punto de venta MP')

    def _compute_current_session(self):
        res = super(PosConfig, self)._compute_current_session()
        for pos_config in self:
            sale_point_id = self.env["pos.box.mp.qr"].sudo().search([("config_id", "=", pos_config.id)], limit=1)
            pos_config.sale_point_id = sale_point_id.id
        return res
