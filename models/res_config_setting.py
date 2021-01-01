from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Res Config Settings'

    discount_journal = fields.Boolean(string="Discount Journal", config_parameter='base_setup.discount_journal')

    account_sale_debit_id = fields.Many2one(comodel_name="account.account", config_parameter='base_setup.account_sale_debit_id', )
    account_sale_credit_id = fields.Many2one(comodel_name="account.account", config_parameter='base_setup.account_sale_credit_id', )
    account_purchase_debit_id = fields.Many2one(comodel_name="account.account", config_parameter='base_setup.account_purchase_debit_id', )
    account_purchase_credit_id = fields.Many2one(comodel_name="account.account", config_parameter='base_setup.account_purchase_credit_id', )


