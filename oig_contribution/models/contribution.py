# models/contribution.py
from odoo import models, fields, api
from datetime import timedelta

class OigContribution(models.Model):
    _name = 'oig.contribution'
    _description = 'OIG Contribution'

    customer_id = fields.Many2one('oig.customer', string='Customer', required=True)
    agent_id = fields.Many2one('oig.agent', string='Agent', related='customer_id.agent_id', store=True)
    amount = fields.Float('Contribution Amount', required=True)
    contribution_date = fields.Date('Contribution Date', default=fields.Date.context_today)
    status = fields.Selection([('paid', 'Paid'), ('pending', 'Pending')], default='pending')

    @api.model
    def create(self, vals):
        """
        Overridden create method to add custom logic whenever a contribution is created.
        """
        contribution = super(OigContribution, self).create(vals)
        
        # Custom logic: Process commissions after creation
        customer = self.env['oig.customer'].browse(vals['customer_id'])
        customer.process_commissions()

        return contribution

    @api.model
    def create_contributions(self, customer_id, contribution_amount):
        customer = self.env['oig.customer'].browse(customer_id)
        daily_amount = customer.daily_contribution_amount
        
        # Calculate how many days the contribution covers
        days_paid = int(contribution_amount // daily_amount)
        remaining_amount = contribution_amount % daily_amount

        contribution_date = fields.Date.context_today(self)
        
        # Create records for each day the contribution covers
        for day in range(days_paid):
            self.create({
                'customer_id': customer.id,
                'agent_id': customer.agent_id.id,
                'amount': daily_amount,
                'contribution_date': contribution_date + timedelta(days=day),
                'status': 'paid',
            })
        
        # If there's a remaining amount, it will be carried over to the next day's contribution
        if remaining_amount > 0:
            self.create({
                'customer_id': customer.id,
                'agent_id': customer.agent_id.id,
                'amount': remaining_amount,
                'contribution_date': contribution_date + timedelta(days=days_paid),
                'status': 'pending',  # Could be pending because it's a partial amount
            })
