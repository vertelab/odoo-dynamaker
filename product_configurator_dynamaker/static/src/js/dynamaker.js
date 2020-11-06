
odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');

    console.log("MyTag")

    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
        if (event.origin === 'https://deployed.dynamaker.com') {
            try {
                const parametersFromDynaMaker = event.data    // Structured data coming from DynaMaker
                
                console.log("parametersFromDynaMaker =", parametersFromDynaMaker)
                
                var x = parametersFromDynaMaker["width"]
                var y = parametersFromDynaMaker["length"]
                var z = parametersFromDynaMaker["thickness"]
                
                var price = self._setProductPrice(x, y, z)
                console.log("price: ", price)
                
                ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', parametersFromDynaMaker).then(
                    function(data) {
                        if (data.error) {
                            console.error(data.error)
                        } else {
                            // calculated price on serverside
                            var price = data['price']
                            console.log("s price: ", price)
                            // $("#output").html(price);
                        }
                    }
                )
          } catch (err) {
            console.warn('Invalid JSON data from DynaMaker')
          }
        }
    })
});

function _setProductPrice(x, y, z) {
    console.log('x = ', x, '; y = ', y, '; z =', z)
    console.log('x * y * z = ', x*y*z)
    
    return x*y*z;
}

/*
 * replaced
 * <t t-call="website_sale.shop_product_carousel"/>
 * with
 * <iframe src='https://deployed.dynamaker.com/applications/kvOWnEY7tMC' id='dynamaker-configurator' width="1000" height="700"></iframe>
 * 
 * 
 * install modules: 'sale_management', 'website_sale (eCommerce)'
 * 
 * "If you edit and save this file, you will never receive updates from Odoo anymore unless you reset your customizations. "
 * 
 * parametersFromDynaMaker = Object { width: 1000, length: 1280, thickness: 10, edgeType: "standard" }
 *
 * */

