{
    'name' : 'Redemption and Point Management - Point Adjustment Module',
    'version' : '1.0',
    'author' : 'JakC',
    'category' : 'Generic Modules/Redemption And Point Management',
    'depends' : ['base_setup','base','jakc_redemption_customer','jakc_redemption_customer_point'],
    'init_xml' : [],
    'data' : [		
        'jakc_redemption_point_adj_view.xml',
        'jakc_redemption_point_adj_menu.xml',
        'security/ir.model.access.csv',                                                  
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}