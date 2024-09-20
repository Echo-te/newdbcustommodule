from odoo import models, fields, api
from datetime import date, timedelta

class OigContribution(models.Model):
    _name = 'oig.contribution'
    _description = 'OIG Contribution'

    service_id = fields.Many2one('oig.service', string='Service', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    amount = fields.Float(string='Amount Contributed', default=lambda self: self.service_id.agreed_amount)
    status = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')], string='Status', default='pending')
    serial_number = fields.Integer(string='Serial Number', compute='_compute_serial_number', store=True)

    @api.depends('service_id.line_ids')
    def _compute_serial_number(self):
        for record in self:
            record.serial_number = len(record.service_id.line_ids) + 1

    @api.onchange('amount')
    def _onchange_amount(self):
        # Logic to handle amount updates, if needed
        pass
