from odoo import models, fields, api
from datetime import timedelta

class OigService(models.Model):
    _name = 'oig.service'
    _description = 'OIG Service'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent', default=lambda self: self.customer_id.agent_id)
    agreed_amount = fields.Float('Agreed Daily Contribution', required=True)
    phone = fields.Char('Phone', related='customer_id.phone', readonly=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    duration_days = fields.Integer('Duration (Days)', compute='_compute_duration')
    total_contributions = fields.Float('Total Amount Contributed', compute='_compute_total_contributions')

    contribution_ids = fields.One2many('oig.contribution', 'service_id', string='Daily Contributions')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days

    @api.depends('contribution_ids')
    def _compute_total_contributions(self):
        for record in self:
            record.total_contributions = sum(contribution.amount for contribution in record.contribution_ids)

    def process_commissions(self):
        # Logic to process commission manually
        for service in self:
            self.env['oig.commission'].create({
                'customer_id': service.customer_id.id,
                'agent_id': service.agent_id.id,
                'amount': service.agreed_amount,
            })
