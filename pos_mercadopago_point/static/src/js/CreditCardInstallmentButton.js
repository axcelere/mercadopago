odoo.define('pos_mercado_point.CreditCardInstallmentButton', function (require) {
'use strict';


    const CreditCardInstallmentPopup = require('pos_credit_card_installment.CreditCardInstallmentPopup');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');

    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;

    class CreditCardInstallmentButton extends CreditCardInstallmentPopup {
        setup() {
            super.setup();
        }
        async onClick() {
            console.log('Test OnClick MP')
            const order = this.env.pos.get_order();
            const installment = this.env.pos.installment;
            if (order.selected_paymentline.payment_method.use_payment_terminal === "mp"){
                if (order.selected_paymentline.amount > 0){
                    rpc.query({
                        model: 'pos.order',
                        method: 'make_payment_mp',
                        args: [[], {'amount_total': order.selected_paymentline.amount, 'payment_method_id': order.selected_paymentline.payment_method.id, 'pos_session_id': order.pos_session_id, 'access_token': order.access_token, 'installment': installment}],
                    }).then(function (vals){
                        if (vals['status_code'] !== 200){
                            Gui.showPopup('ErrorPopup', {
                                title: _t('Error'),
                                body: _t(vals['error']),
                            });
                        }
                        else{
                            localStorage['access_token_payment'] = vals['access_token']
                        }
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
                        method: 'make_refunds',
                        args: [[], {'amount_total': order.selected_paymentline.amount, 'payment_method_id': order.selected_paymentline.payment_method.id, 'pos_session_id':order.pos_session_id, 'toRefundLines_ids': toRefundLines_ids}],
                    }).then(function (vals){
                        if (vals['status_code'] !== 200){
                            Gui.showPopup('ErrorPopup', {
                                title: _t('Error'),
                                body: _t(vals['error']),
                            });
                        }
                        else{
                            localStorage['access_token_payment'] = vals['access_token']
                        }
                    });
                }
            }else{
                await super.onClick();
            }
        }

    }

    CreditCardInstallmentButton.template = 'CreditCardInstallmentButton';
    Registries.Component.add(CreditCardInstallmentButton);
    return CreditCardInstallmentButton;

});
