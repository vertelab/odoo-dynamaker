/*
  Catching DynaMaker events and passing them on to Odoo Product Configurator (PLEDRA)
*/
odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');
    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
        // Action for DynaMaker on event
        if (event.origin === 'https://deployed.dynamaker.com') {

            try {
                const parametersFromDynaMaker = event.data    
                if (parametersFromDynaMaker instanceof Blob){ 
                     var reader = new FileReader();
                     reader.readAsDataURL(parametersFromDynaMaker); 
                     reader.onloadend = function() {
                         var base64data = reader.result;                
                         ajax.jsonRpc('/dynamaker/drawing', 'call', {
                             blobFile: base64data, qty: 1
                             }).then(function(data) { 
                                    document.querySelector("input[data-attribute_value_name='drawing']").value = data.attachment_id
                                    
                                 });
                        }
                    }
                 else {
                    for (var key in parametersFromDynaMaker) {
                        console.log(parametersFromDynaMaker[key]);
                        if (parametersFromDynaMaker.hasOwnProperty(key)) {
                            document.querySelector("input[data-attribute_value_name='" + key + "']").value = parametersFromDynaMaker[key]
                        }
                    }               
                    parametersFromDynaMaker.product_id = document.querySelector("h1[data-oe-id]").getAttribute("data-oe-id")
                    ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', {custom_values: parametersFromDynaMaker, qty: 1}).then(function(data) {
                        if (data.error) {
                            console.error(data.error)
                        } else {
                            console.log(data)
                            $('span.oe_currency_value').text(data.price)
                            $(document.getElementsByClassName("product_price mt16"))[0].setAttribute('class','product_price mt16')
                            $(document.getElementById("add_to_cart").removeAttribute('style'))
                        }
                    })
                }
            } catch (err) {
                console.warn('Invalid JSON data from DynaMaker')
                console.warn(err)
            }
        }
    })
    $(document).ready(function(){
        let iframe = $('iframe#dynamaker-configurator');
        iframe.attr('src', iframe.data('src'));
    });
    $("body").on("click",".a-submit-dynamaker", function(ev){
        var iframeWin = document.getElementById("dynamaker-configurator").contentWindow;
        iframeWin.postMessage("send event to dynamaker", "https://deployed.dynamaker.com");
    });
})

/*
 * parametersFromDynaMaker = Object { width: 1000, length: 1280, thickness: 10, edgeType: "standard" }
 */
