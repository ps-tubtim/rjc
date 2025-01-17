# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api


class AccountPaymentIntransit(models.Model):
    _inherit = 'account.payment.intransit'

    bank_journal_id = fields.Many2one(
        required=False,
    )


class AccountPaymentIntransitLine(models.Model):
    _inherit = 'account.payment.intransit.line'

    due_date = fields.Date()
    bank_branch = fields.Char(
        string='Bank/Branch',
    )
    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string='Payment Reference',
        copy=False,
    )

    @api.onchange('receipt_type')
    def onchange_receipt_type(self):
        payment_id = self._context.get('payment_id', False)
        if payment_id:
            self.move_line_id = self.env['account.move.line'].search([
                ('payment_id', '=', payment_id),
                ('reconciled', '=', False),
                ('debit', '>', 0)])
