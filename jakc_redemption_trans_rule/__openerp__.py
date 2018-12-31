{
    'name' : 'Redemption and Point Management - Trans Rule Module',
    'version' : '1.0',
    'author' : 'JakC',
    'category' : 'Generic Modules/Redemption And Point Management',
    'depends' : ['base_setup','base','jakc_redemption','jakc_redemption_customer','jakc_redemption_tenant'],
    'init_xml' : [],
    'data' : [			
        'security/ir.model.access.csv',        
        'jakc_redemption_trans_rule_view.xml',
        'jakc_redemption_trans_rule_menu.xml',            
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}