{
    'name' : 'Redemption and Point Management - Tenant Module',
    'version' : '1.0',
    'author' : 'JakC',
    'category' : 'Generic Modules/Redemption And Point Management',
    'depends' : ['base_setup','base','jakc_redemption','jakc_redemption_customer'],
    'init_xml' : [],
    'data' : [		
        'security/ir.model.access.csv',	        
        'jakc_redemption_tenant_view.xml',    
        'jakc_redemption_tenant_menu.xml',      
        'jakc_redemption_customer_view.xml',          
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}