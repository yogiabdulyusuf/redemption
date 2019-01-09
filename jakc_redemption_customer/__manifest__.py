{
    "name" : "Redemption and Point Management - Customer Module",
    "version": "10.0.1.0",
    "author" : "JakC",
    "category" : "Generic Modules/Redemption And Point Management",
    "depends" : ["base_setup","base","jakc_redemption"],
    "init_xml" : [],
    "data" : [	
        "view/jakc_redemption_customer_view.xml",
        "view/jakc_redemption_customer_config_view.xml",
        "view/jakc_redemption_customer_menu.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}