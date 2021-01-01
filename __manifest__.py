# -*- coding: utf-8 -*-
{
    'name': "discount_journal",
    'summary': """Discount Journal""",
    'description': """Create journal for discount in sale and purchase""",
    'author': "",
    'category': 'Uncategorized',
    'version': '13.0.0.1',
    'depends': ['base','account', 'sale', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/res_config_setting.xml',
    ],

}
