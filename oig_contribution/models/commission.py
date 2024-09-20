from odoo import models, fields, api

class OigCommission(models.Model):
    _name = 'oig.commission'
    _description = 'OIG Commission'

   
    customer_id = fields.Many2one('oig.customer', string='Customer', required=True)
    service_id = fields.Many2one('oig.service', string='Service', required=True)
    commission_amount = fields.Float(string='Commission Amount', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], string='Status', default='pending')

    @api.depends('service_id.total_contributed')
    def _compute_amount(self):
        for record in self:
            record.amount = record.service_id.agreed_amount  # 1-day equivalent

    def process_commission_automatically(self):
        """ Scheduled action for automatic commission processing at the end of the 31 days """
        services = self.env['oig.service'].search([])
        for service in services:
            if not service.commission_id and service.duration >= 31:
                daily_contribution = service.agreed_amount / 31
                self.create({
                    'agent_id': service.agent_id.id,
                    'customer_id': service.customer_id.id,
                    'service_id': service.id,
                    'commission_amount': daily_contribution,
                    'status': 'paid'
                })

    @api.model
    def create(self, vals):
        commission_amount = vals.get('commission_amount', 0.0)
        if 'service_id' in vals:
            service = self.env['oig.service'].browse(vals['service_id'])
            service.total_amount += commission_amount  # Update total amount on the service
        return super(OigCommission, self).create(vals)
