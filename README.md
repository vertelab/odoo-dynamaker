# odoo-dynamaker
Dynamaker plugin

## how to setup dynamaker skateboard
* If dynamaker is not installed: run odoogitclone odoo-dynamaker

* If dynamaker is not installed: go to debug mode -> update module list

* GO TO Apps and install modules:
    * sale_management
    * website_sale (eCommerce)
    * product_configurator_dynamaker

* GO TO Sales > Products > Products > Customizable Desk (CONFIG) > Edit:
   * Check the "Dynamaker Product" checkbox
   * Enter as Dynamaker URL: https://deployed.dynamaker.com/applications/kvOWnEY7tMC
   * Enter arbitrary price algorithm, e.g: price = kw['width'] * kw['length']
   * Save.

* On the same page, go to the variants tab
   * Remove all existsing variants (Legs and Color)
   * Add these lines: (it is important that the value name here is the same as the name recieved from dynamaker)
      * Attribute Name: Width, Display Type: Hidden Text, Value: width, Is custom value (the checkbox): checked
      * Attribute Name: Length, Display Type: Hidden Text, Value: length, Is custom value (the checkbox): checked
      * Attribute Name: Thickness, Display Type: Hidden Text, Value: thickness, Is custom value (the checkbox): checked
      * Attribute Name: EdgeType, Display Type: Hidden Text, Value: edgeType, Is custom value (the checkbox): checked
   * Add the values to the attributes
   * Save.

* From there, GO TO > "Go to website" > Customize > HTML/CSS/JS > copy-and-paste to browser:
    * XML: /usr/share/odoo-delivery/product_configurator_dynamaker/views/lukas_view.xml
    * JS: /usr/share/odoo-delivery/product_configurator_dynamaker/static/src/js/dynamaker.js
    
* Run odoorestart; odootail

* Bob's your uncle
