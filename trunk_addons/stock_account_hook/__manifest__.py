# Copyright 2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "COP Stock Account Hook",
    "summary": "Add a hook to create a unique account move for valuation layer in/out process",
    "author": "Copelme S.A.",
    "version": "16.0.1.0.3",
    "category": "Warehouse Management",
    "website": "http://copelme.com",
    "license": "LGPL-3",
    "depends": ["stock_account"],
    "data":[
        'views/res_config_settings_views.xml',
        'views/stock_picking_views.xml',
    ],
    "installable": True,
    "auto_install": False,
    "post_load": "post_load_hook",
}
