# models/commission.py
from odoo import models, fields, api
from datetime import date, timedelta

class OigCommission(models.Model):
    _name = 'oig.commission'
    _description = 'OIG Commission'

    customer_id = fields.Many2one('oig.customer', string='Customer', required=True)
    agent_id = fields.Many2one('oig.agent', string='Agent', related='customer_id.agent_id', store=True)
    commission_amount = fields.Float('Commission Amount', compute='_compute_commission')
    contribution_period_start = fields.Date('Contribution Period Start', required=True)
    contribution_period_end = fields.Date('Contribution Period End', required=True)

    @api.depends('customer_id', 'customer_id.daily_contribution_amount', 'contribution_period_start', 'contribution_period_end')
    def _compute_commission(self):
        """
        Calculate the commission as one day's contribution for every month.
        If the customer doesn't complete the cycle, OIG still takes one day's contribution as commission.
        """
        for record in self:
            total_contributions = self.env['oig.contribution'].search_count([
                ('customer_id', '=', record.customer_id.id),
                ('contribution_date', '>=', record.contribution_period_start),
                ('contribution_date', '<=', record.contribution_period_end)
            ])
            
            if total_contributions >= 31:
                # Full month cycle: Commission is one day’s contribution
                record.commission_amount = record.customer_id.daily_contribution_amount
            else:
                # Incomplete cycle: Still take one day’s worth of contribution as commission
                record.commission_amount = record.customer_id.daily_contribution_amount

    def process_commissions(self):
        """ Process commissions for all customers """
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        customers = self.env['oig.customer'].search([])
        for customer in customers:
            # Check if customer has completed the month's contributions
            self.env['oig.commission'].create({
                'customer_id': customer.id,
                'agent_id': customer.agent_id.id,
                'contribution_period_start': start_of_month,
                'contribution_period_end': end_of_month,
            })

        return True

