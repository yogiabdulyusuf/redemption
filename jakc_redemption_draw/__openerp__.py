{
    'name' : 'Redemption and Point Management - Draw Module',
    'version' : '1.0',
    'author' : 'Wahyu Hidayat',
    'category' : 'Generic Modules/Redemption And Point Management',
    'depends' : ['base_setup','base','jakc_redemption_schemas'],
    'init_xml' : [],
    'data' : [			
       'jakc_redemption_draw_view.xml',
       'jakc_redemption_schemas_view.xml',
       'jakc_redemption_draw_menu.xml',                 
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}