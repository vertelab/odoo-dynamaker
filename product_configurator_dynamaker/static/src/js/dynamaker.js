/*
  Catching DynaMaker events and passing them on to Odoo Product Configurator (PLEDRA)
*/
odoo.define("dynamaker_integration_experiment.dynamaker_price_integration", function(require) {
    "use strict";
    var ajax = require('web.ajax');

    console.log(getEvents())

    // Define listener for DynaMaker Events
    window.addEventListener('message', (event)=>{
        console.log("event: ", event)
        // Action for DynaMaker on event
        if (event.origin === 'https://deployed.dynamaker.com') {
            try {
                const parametersFromDynaMaker = event.data    // Structured data coming from DynaMaker
                
                for (var key in parametersFromDynaMaker) {
                    if (parametersFromDynaMaker.hasOwnProperty(key)) {
                        document.querySelector("input[data-attribute_value_name='" + key + "']").value = parametersFromDynaMaker[key]
                    }
                }
                
                parametersFromDynaMaker.product_id = document.querySelector("h1[data-oe-id]").getAttribute("data-oe-id");
                
                ajax.jsonRpc('/product_configurator/dynamaker_price', 'call', parametersFromDynaMaker).then(function(data) {
                    if (data.error) {
                        console.error(data.error)
                    } else {
                        $('span.oe_currency_value').text(data.price)
                    }
                })
            } catch (err) {
                console.warn('Invalid JSON data from DynaMaker')
                console.warn(err)
            }
        }
    })
})

$( document ).ready(function() {
    const event = new Event('Initial');
    event.data = {}
    
    window.dispatchEvent(event);
});

/*
 * parametersFromDynaMaker = Object { width: 1000, length: 1280, thickness: 10, edgeType: "standard" }
 */

function getEvents() {
    const result = {}
    
    result['window'] = _getEvents(window, hasOwnProperty);
    
    const arr = Object.getOwnPropertyNames(window);
    
    for (let i = 0; i < arr.length; i++) {
        const element = arr[i];
        
        let resultArray = [];
        
        try {
            const obj = window[element];
            
            if (!obj || !obj["prototype"]) {
                continue;
            }
            
            proto = obj["prototype"];
            resultArray = _getEvents(proto);
        }
        catch (err) {
            console.err("failed to get events");
        }
        result[element] = resultArray;
    }
    
    return result;
}































