from odoo import models, fields, api
from datetime import timedelta

class OigService(models.Model):
    _name = 'oig.service'
    _description = 'OIG Service'

    customer_id = fields.Many2one('oig.customer', string='Customer', required=True)
    agreed_amount = fields.Float(string='Agreed Contribution Amount', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    duration = fields.Integer(string='Duration (days)', default=31)
    line_ids = fields.One2many('oig.contribution', 'service_id', string='Contributions')
    total_contributed = fields.Float(string='Total Contributed', compute='_compute_total_contributed')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    @api.depends('start_date')
    def _compute_end_date(self):
        for service in self:
            if service.start_date:
                service.end_date = service.start_date + timedelta(days=service.duration)
            else:
                service.end_date = False

    @api.depends('line_ids.amount')
    def _compute_total_contributed(self):
        for service in self:
            service.total_contributed = sum(line.amount for line in service.line_ids)

    @api.depends('total_contributed')
    def _compute_total_amount(self):
        for service in self:
            service.total_amount = service.total_contributed