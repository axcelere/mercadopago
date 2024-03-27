odoo.define('pos_mercadopago_qr.CreditCardInstallmentButton', function (require) {
'use strict';


    const CreditCardInstallmentButton = require('pos_credit_card_installment.CreditCardInstallmentButton');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');

    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;

    const CreditCardInstallmentButtonMP = CreditCardInstallmentButton => class extends CreditCardInstallmentButton {

        /**
         * @override
         */
        async onClick() {
            const order = this.env.pos.get_order();
            const installment = this.env.pos.installment;
            if (order.selected_paymentline.payment_method.use_payment_terminal === "mp_qr"){
                console.log('Test MPQR ENTRO')
                console.log(order)
                if (order.selected_paymentline.amount > 0){
                    // const orderlines = order.orderlines
                    // let info_line = []
                    // _.each(orderlines, function(line_id,index) {
                    //     info_line.push({"title": line_id.product.display_name,
                    //                     "unit_price": line_id.price,
                    //                     "quantity": line_id.quantity,
                    //                     "description": line_id.product.display_name,
                    //     });
                    // })
                    // 'info_product': info_line,
                    rpc.query({
                        model: 'pos.order',
                        method: 'make_payment_mp_qr',
                        args: [[], {'amount_total': order.selected_paymentline.amount,
                                    'payment_method_id': order.selected_paymentline.payment_method.id,
                                    'pos_session_id': order.pos_session_id,
                                    'access_token': order.access_token,
                                    'installment': installment,
                                    'order_name': order.name,
                                    'order_uid': order.uid,
                        }],
                    }).then(function (vals){
                        if (vals['status_code'] !== 200){
                            Gui.showPopup('ErrorPopup', {
                                title: _t('Error'),
                                body: _t(vals['error']),
                            });
                        }
                        // else{
                        //     localStorage['access_token_payment'] = vals['access_token']
                        //     order.mp_qr_payment_token = vals['access_token']
                        // }
                    });
                }
                else{
                    const toRefundLines = this.env.pos.toRefundLines
                    let toRefundLines_ids = []
                    _.each(toRefundLines, function(line_id,index) {
                        toRefundLines_ids.push(line_id.orderline.orderBackendId);
                    })
                    rpc.query({
                        model: 'pos.order',
                        method: 'make_refunds_mp',
                        args: [[], {'amount_total': order.selected_paymentline.amount, 'payment_method_id': order.selected_paymentline.payment_method.id, 'pos_session_id':order.pos_session_id, 'toRefundLines_ids': toRefundLines_ids}],
                    }).then(function (vals){
                        if (vals['status_code'] !== 200){
                            Gui.showPopup('ErrorPopup', {
                                title: _t(vals['error']),
                                body: _t(vals['message']),
                            });
                        }
                        else{
                            localStorage['access_token_payment'] = vals['access_token']
                            order.mp_qr_payment_token = vals['access_token'];
                        }
                    });
                }
            }else{
                await super.onClick();
            }
        }

    }

    // CreditCardInstallmentButtonMP.template = 'CreditCardInstallmentButtonMP';
    // Registries.Component.add(CreditCardInstallmentButtonMP);
    // return CreditCardInstallmentButtonMP;
    Registries.Component.extend(CreditCardInstallmentButton, CreditCardInstallmentButtonMP);
    return CreditCardInstallmentButton;

});
