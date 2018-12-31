{
    'name' : 'Redemption and Point Management - Customer Coupon Module',
    'version' : '1.0',
    'author' : 'JakC',
    'category' : 'Generic Modules/Redemption And Point Management',
    'depends' : ['base_setup','base','jakc_redemption','jakc_redemption_customer'],
    'init_xml' : [],
    'data' : [	
        'security/ir.model.access.csv',	
        'jakc_redemption_customer_coupon_view.xml',
        'jakc_redemption_customer_coupon_scheduler.xml',                
        'jakc_redemption_customer_view.xml',              
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}