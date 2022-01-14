/*
  Catching DynaMaker events and passing them on to Odoo Product Configurator (PLEDRA)
*/
odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');
    // Define listener for DynaMaker Events
    window.addEventListener('message', (event) => {
        // Action for DynaMaker on event
        if (event.origin === 'https://deployed.dynamaker.com') {
            try {
                const parametersFromDynaMaker = event.data
                for (const [k, value] of Object.entries(parametersFromDynaMaker)) {
                    if (k === 'mrpData') {

                        for (var key in value['quantities']) {
                            if (value['quantities'].hasOwnProperty(key)) {
                                document.querySelector("input[data-attribute_value_name='" + key + "']").value = value['quantities'][key]
                            }
                        }
                        let drawings = []
                    // value= { quantities: {…}, drawings: {…} }
                    const toBase64 = file => new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.readAsDataURL(file);
                        reader.onload = () => resolve(reader.result);
                        reader.onerror = error => reject(error);
                    });

                    async function readDynamakerData(drawingName,dynamakerData) {
                        const file = dynamakerData;
                        const a = await toBase64(file);

                        console.log('a' + a)
                        drawings.push({
                                    [drawingName]: a,
                                })
                     }
                        var reader = new FileReader();
                        for (const [drawingName, drawingVal] of Object.entries(value['drawings'])) {
                                   readDynamakerData(drawingName, drawingVal)
                        }

                        setTimeout(() => {

                                                 value['drawings'] = drawings
                        ajax.jsonRpc('/dynamaker/mrpdata', 'call', {
                            mrpData: value,
                            qty: 1
                        }).then(function(data) {
                            document.querySelector("input[data-attribute_value_name='drawing']").value = data.attachment_id
                            console.log('attachments ids:::::  ',data.attachment_id)
                                        console.log('Here 4')
                            document.getElementById("add_to_cart").click();
                        });
                         }, 500);

                    } else {
                        for (var key in parametersFromDynaMaker) {
                            console.log(parametersFromDynaMaker[key]);
                            if (parametersFromDynaMaker.hasOwnProperty(key)) {
                                document.querySelector("input[data-attribute_value_name='" + key + "']").value = parametersFromDynaMaker[key]
                            }
                        }
                        parametersFromDynaMaker.product_id = document.querySelector("h1[data-oe-id]").getAttribute("data-oe-id")
                        ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', {
                            custom_values: parametersFromDynaMaker,
                            qty: 1
                        }).then(function(data) {
                            if (data.error) {
                                console.error(data.error)
                            } else {
                                console.log(data)
                                $('span.oe_currency_value').text(data.price)
                                $(document.getElementsByClassName("product_price mt16"))[0].setAttribute('class', 'product_price mt16')
                                $(document.getElementById("add_to_cart").removeAttribute('style'))
                            }
                        })
                    }
                }
            } catch (err) {
                console.warn('Invalid JSON data from DynaMaker')
                console.warn(err)
            }
        }
    })

    $(document).ready(function() {
        let iframe = $('iframe#dynamaker-configurator');
        iframe.attr('src', iframe.data('src'));
    });
    $("body").on("click", ".a-submit-dynamaker", function(ev) {
        var iframeWin = document.getElementById("dynamaker-configurator").contentWindow;
        iframeWin.postMessage("send event to dynamaker", "https://deployed.dynamaker.com");
    });
})
