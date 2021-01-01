from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    discount_total = fields.Float(string='Discount Total', compute='_compute_discount_total')

    @api.depends('invoice_line_ids')
    def _compute_discount_total(self):
        for rec in self:
            total_discount = 0.0
            for line in rec.invoice_line_ids:
                if self.env['ir.config_parameter'].sudo().get_param('base_setup.discount_journal') == "True":
                    if line.discount > 0:
                        total_discount += line.quantity * line.price_unit * line.discount /100
            rec.discount_total = total_discount

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.env['ir.config_parameter'].sudo().get_param('base_setup.discount_journal') == "True":
            if self.invoice_origin:
                if 'S' in self.invoice_origin:
                    if self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_credit_id') is False:
                        raise ValidationError(_('Enter Sale Credit Account in Setting'))
                    if self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_debit_id') is False:
                        raise ValidationError(_('Enter Sale Debit Account in Setting'))
                    credit_line_vals = {
                        'move_id': self.id,
                        'exclude_from_invoice_tab': True,
                        'name': 'Debit Discount For Sale '+ self.invoice_origin,
                        'account_id': int(self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_debit_id')),
                        'debit': 0.0,
                        'credit': self.discount_total
                    }
                    debit_line_vals = {
                        'move_id': self.id,
                        'exclude_from_invoice_tab': True,
                        'name': 'Credit Discount For Sale ' + self.invoice_origin,
                        'account_id': int(self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_credit_id')),
                        'credit': 0.0,
                        'debit': self.discount_total
                    }

                    # vals = [credit_line_vals,  debit_line_vals]
                    self.write({
                     'line_ids': [
                         (0, 0,credit_line_vals),
                         (0, 0, debit_line_vals),
                     ],
                    })

            if self.purchase_id:
                if self.env['ir.config_parameter'].sudo().get_param('base_setup.account_purchase_credit_id') is False:
                    raise ValidationError(_('Enter Purchase Credit Account in Setting'))
                if self.env['ir.config_parameter'].sudo().get_param('base_setup.account_purchase_debit_id') is False:
                    raise ValidationError(_('Enter Purchase Debit Account in Setting'))
                credit_line_vals = {
                    'move_id': self.id,
                    'exclude_from_invoice_tab': True,
                    'name': 'Debit Discount For Purchase ' + self.purchase_id.name,
                    'account_id': int(self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_debit_id')),
                    'debit': 0.0,
                    'credit': self.discount_total
                }
                debit_line_vals = {
                    'move_id': self.id,
                    'exclude_from_invoice_tab': True,
                    'name': 'Credit Discount For Purchase ' + self.purchase_id.name,
                    'account_id': int(self.env['ir.config_parameter'].sudo().get_param('base_setup.account_sale_debit_id')),
                    'credit': 0.0,
                    'debit': self.discount_total
                }

                # vals = [credit_line_vals,  debit_line_vals]
                self.write({
                 'line_ids': [
                     (0, 0,credit_line_vals),
                     (0, 0, debit_line_vals),
                 ],
                })
        return res



