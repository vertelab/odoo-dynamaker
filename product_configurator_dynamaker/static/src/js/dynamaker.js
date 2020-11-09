odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');

    console.log("MyTag")

    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
        if (event.origin === 'https://deployed.dynamaker.com') {
            try {
                // gets parameters from Dynamaker
                const parametersFromDynaMaker = event.data    
                console.log("parametersFromDynaMaker =", parametersFromDynaMaker)
                
                // calculate price on client side
                var x = parametersFromDynaMaker["width"]
                var y = parametersFromDynaMaker["length"]
                var z = parametersFromDynaMaker["thickness"]
                var price = self._setProductPrice(x, y, z)
                console.log("client price: ", price)
                
                // calculate price on serverside
                ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', parametersFromDynaMaker).then(function(data) {
                    if (data.error) {
                        console.error(data.error)
                    } else {
                        console.log("server price: ", data['price'])
                    }
                })
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

/* OLD CODE:
 odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');

    console.log("MyTag")

    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
          // Action for DynaMaker on event
          if (event.origin === 'https://deployed.dynamaker.com') {
            try {
              const parametersFromDynaMaker = event.data    // Structured data coming from DynaMaker

              ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', parametersFromDynaMaker).then(function(data) {
                if (data.error) {
                  console.error(data.error)
                } else {
                  var values = data.value
                  var domains = data.domain
                  var open_cfg_step_line_ids = data.open_cfg_step_line_ids
                  var config_image_vals = data.config_image_vals
                  self._applyDomainOnValues(domains)
                  self._setDataOldValId()
                  self._handleOpenSteps(open_cfg_step_line_ids)
                  self._setImageUrl(config_image_vals)
                  self._setWeightPrice(values.weight, values.price, data.decimal_precision)
                }
              })
          } catch (err) {
            console.warn('Invalid JSON data from DynaMaker')
          }

        }
    })
});
 */
