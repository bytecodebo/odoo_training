# -*- coding: utf-8 -*-
{
    'name': "Byc Report Creator",
    'summary': """
        With this module you can generate report  xls,csv and pdf without coding
        """,

    'description': """
        With this module you can generate report  xls,csv and pdf without coding,
        for more development you can email me @alfatihridhont@gmail.com
    """,

    'author': "Alfatih Ridho NT",
    'website': "alfatihridhont@gmail.com",
    'category': 'Report',
    'license': 'AGPL-3',
    'version': '16.0.2.1',
    'support': 'alfatihridhont@gmail.com',
    'images': ['static/src/img/icon.png'],
    'depends': [
        #'odoo_dynamic_dashboard',
        #'mass_editing',
        #'calendar',
        #'snailmail',
        'report_xlsx',
        # 'reports_with_watermark',
        # 'web_ir_actions_act_window_message',
        # 'report_wkhtmltopdf_param',
        #'web_confirm_on_save',
        #'inputmask_widget',
        #'byc_web_crud_buttons',
        # 'web_company_color',
        #'w_disable_debug_mode',
        #'simple_readonly_user',
        # 'byc_backend_printer'
    ],
    'external_dependencies': {
        'python': ['pdfkit', 'xlwt', ]
    },
    'data': [
        # 'data/res_users_data.xml',
        'data/data.xml',
        'security/groups_security.xml',
        # 'security/role_groups_security.xml',
        # 'security/ir.model.access.csv',
        'security/user/ir.model.access.csv',
        'security/manager/ir.model.access.csv',
        # 'views/assets.xml',
        # 'views/ir_actions_views.xml',
        # 'views/document_layout_views.xml',
        'views/views.xml',
        'views/res_config_settings.xml',
        'wizard/wizard_get_report.xml',
        # 'views/report_menuitem.xml',
        # 'views/report_templates.xml',
        #'views/report_watermark_templates.xml',
        # 'views/report_templates_roll.xml',
        'views/menu_items.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'cop_report_creator/static/src/js/pdf_preview.js',
            # 'byc_report_creator/static/src/js/field_pdf_preview_widget.js',
            'byc_report_creator/static/src/xml/widget_template.xml',
            'byc_report_creator/static/src/scss/modal.scss'
        ]
    },
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
