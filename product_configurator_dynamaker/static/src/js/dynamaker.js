
odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');

    console.log("MyTag")

    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
        if (event.origin === 'https://deployed.dynamaker.com') {
            try {
                const parametersFromDynaMaker = event.data    // Structured data coming from DynaMaker

                ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', parametersFromDynaMaker).then(
                    function(data) {
                        if (data.error) {
                            console.error(data.error)
                        } else {
                            var x = data.dimensions['x']
                            var y = data.dimensions['y']
                            var z = data.dimensions['z']
                            var edge_type = data.edge_type
                            
                            self._setProductPrice(x, y, z)
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
    return 5;
}

/*
 * replaced
 * <t t-call="website_sale.shop_product_carousel"/>
 * 
 * with
 * <iframe src='https://deployed.dynamaker.com/applications/kvOWnEY7tMC' id='dynamaker-configurator' width="1000" height="700"></iframe>
 * 
 * 
 * installera 'sale_management', 'website_sale (eCommerce)'
 * 
 * 
 * "If you edit and save this file, you will never receive updates from Odoo anymore unless you reset your customizations. "
 * 
 * parametersFromDynaMaker = Object { width: 1000, length: 1280, thickness: 10, edgeType: "standard" }
 * * 
 * */

