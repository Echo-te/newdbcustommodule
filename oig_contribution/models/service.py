from odoo import models, fields, api

class OigService(models.Model):
    _name = 'oig.service'
    _description = 'OIG Service'

    customer_id = fields.Many2one('oig.customer', string='Customer', required=True)
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent', related='customer_id.agent_id', store=True)
    agreed_amount = fields.Float(string='Agreed Contribution Amount', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(string='Duration (days)', compute='_compute_duration', store=True)
    line_ids = fields.One2many('oig.contribution', 'service_id', string='Contributions')
    total_contributed = fields.Float(string='Total Contributed', compute='_compute_total_contributed')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for service in self:
            if service.start_date and service.end_date:
                service.duration = (service.end_date - service.start_date).days
            else:
                service.duration = 0

    @api.depends('line_ids.amount')
    def _compute_total_contributed(self):
        for service in self:
            service.total_contributed = sum(line.amount for line in service.line_ids)

    def action_process_commission(self):
        # Process the commission for the service
        pass
