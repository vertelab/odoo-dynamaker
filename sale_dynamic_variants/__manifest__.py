# -*- coding: utf-8 -*-


{
    'name': 'Product Dynamic Variant',
    'version': '1.0',
    'category': 'Sales',
    'description': """
This module adds dynamic variants
=================================

Adds A variant type to Product Template that:
--------------------------------------
    * Can store a float (other data types in future)
    * Store the data on sale.order.line
    * Can compute a price due to dynamic changes
    
    """,
    'depends': ['product'],
    'data': [
        'views/product_views.xml',
        
    ],
    'website': 'https://www.vertel.se/module/product_dynamic_variant',
}
