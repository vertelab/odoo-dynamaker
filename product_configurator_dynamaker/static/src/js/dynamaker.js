/*
  Catching DynaMaker events and passing them on to Odoo Product Configurator (PLEDRA)
*/
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
                   $('span.oe_currency_value').text(data.price)
                }
              })
          } catch (err) {
            console.warn('Invalid JSON data from DynaMaker')
          }

        }
    })
})

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
