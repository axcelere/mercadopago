odoo.define('pos_payway.PaymentScreen', function (require) {
    'use strict';

    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { Gui } = require('point_of_sale.Gui');
    const Dialog = require('web.Dialog');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;

    const PosPaywayPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            /**
             * @override
             */

            async validateOrder(isForceValidate) {
                NumberBuffer.capture();
                let payment_type;
                const order = this.env.pos.get_order();
                const installment = this.env.pos.installment;
                if (order.selected_paymentline.payment_method.use_payment_terminal === "mp_qr"){
                    if (order.selected_paymentline.amount > 0){
                        payment_type = 'payments'
                    }
                    else{
                        payment_type = 'reversals_refunds'
                    }
                    var result = await rpc.query({
                        model: 'pos.order',
                        method: 'get_payment_status_mp',
                        args: [[], {'amount_total': order.selected_paymentline.amount, 'payment_method_id': order.selected_paymentline.payment_method.id, 'pos_session_id': order.pos_session_id, 'access_token_payment': localStorage['access_token_payment'], 'payment_type_build': payment_type, 'installment': installment}],
                    });

                    if ((result['payment_status'] === 'CONFIRMED' || result['payment_status'] === 'REVERSED') && result['status_code'] === 200){
                        var result_new = await super.validateOrder(...arguments);
                        return rpc.query({
                            model: 'pos.order',
                            method: 'updating_order',
                            args: [[], { 'access_token_payment': localStorage['access_token_payment'], 'access_token_order': order.access_token}],
                        });
                    }
                    if ((result['payment_status'] !== 'CONFIRMED' || result['payment_status'] === 'REVERSAL_REQUEST') && result['status_code'] === 200){
                        Gui.showPopup('ErrorPopup', {
                            title: _t('Aviso'),
                            body: _t('Debe ser realizada la transacción antes de ser validada!'),
                        });
                    }
                    if (result['status_code'] !== 200){
                        Gui.showPopup('ErrorPopup', {
                            title: _t('Error'),
                            body: _t(vals['error']),
                        });
                    }
                }
                else{
                    return super.validateOrder(...arguments);
                }
            }

            deletePaymentLine(event) {
                var self = this;
                const { cid } = event.detail;
                let payment_type;

                const line = this.paymentLines.find((line) => line.cid === cid);
                console.log('testfffff')
                console.log(line)
                if (line.payment_method.use_payment_terminal === "mp_qr"){
                    try {
                        rpc.query({
                            model: 'pos.order',
                            method: 'make_cancel_mp',
                            args: [[], {'amount_total': line.amount, 'payment_method_id': line.payment_method.id, 'pos_session_id':line.order.pos_session_id, 'access_token_payment': localStorage['access_token_payment']}],
                        });
                    } catch (_e) {
                        Dialog.alert(this, _t("Error trying to connect to terminal. Check your internet connection"));
                    }}

                // If a paymentline with a payment terminal linked to
                // it is removed, the terminal should get a cancel
                // request.
                if (['waiting', 'waitingCard', 'timeout'].includes(line.get_payment_status())) {
                    line.set_payment_status('waitingCancel');
                    line.payment_method.payment_terminal.send_payment_cancel(this.currentOrder, cid).then(function() {
                        self.currentOrder.remove_paymentline(line);
                        NumberBuffer.reset();
                        self.render(true);
                    })
                }
                else if (line.get_payment_status() !== 'waitingCancel') {
                    this.currentOrder.remove_paymentline(line);
                    NumberBuffer.reset();
                    this.render(true);
                }
            }
    };
    Registries.Component.extend(PaymentScreen, PosPaywayPaymentScreen);
    return PaymentScreen;
    });
