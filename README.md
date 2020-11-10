# odoo-dynamaker
Dynamaker plugin

## how to setup dynamaker skateboard
* run odoogitclone odoo-dynamaker

* go to debug mode -> update module list

* install modules:
    * sale_management
    * website_sale (eCommerce)
    * product_configurator_dynamaker

* GO TO Sales > Products > Products > Customizable Desk (CONFIG) > "Go to website" > Customize > HTML/CSS/JS > copy-and-paste to browser:
    * XML: product_configurator_dynamaker/views/lukas_view.xml
    * JS: product_configurator_dynamaker/static/src/js/dynamaker.js
    
* run odoorestart; odootail

* Bob's your uncle
