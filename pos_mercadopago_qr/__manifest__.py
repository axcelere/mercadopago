# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MP QR',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Payment method MP',
    'description': """
Allow to pay with Payway
==============================

This module allows customers to pay for their orders with credit
cards. The transactions are processed by MP (developed by Axcelere). 
    """,
    'depends': ['point_of_sale', 'pos_credit_card_installment'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_mp_views.xml',
        'views/pos_store_views.xml',
        'views/pos_config_setting_views.xml',
        'views/pos_box_views.xml',
    ],
    'demo': [
        'data/pos_mp_demo.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'pos_mercadopago_qr/static/src/js/PaymentScreen.js',
            'pos_mercadopago_qr/static/src/js/CreditCardInstallmentButton.js',
        ],
    },
    'license': 'LGPL-3',
}
