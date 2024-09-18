# models/agent.py
from odoo import models, fields
from datetime import date, timedelta

class OigAgent(models.Model):
    _name = 'oig.agent'
    _description = 'OIG Agent'

    name = fields.Char('Name', required=True)
    location = fields.Char('Location')
    customer_ids = fields.One2many('oig.customer', 'agent_id', string='Customers Managed')
    daily_collections_ids = fields.One2many('oig.contribution', 'agent_id', string='Daily Collections')


    def process_commissions(self):
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        for customer in self.customer_ids:
            existing_commission = self.env['oig.commission'].search([
                ('customer_id', '=', customer.id),
                ('contribution_period_start', '=', start_of_month),
                ('contribution_period_end', '=', end_of_month),
            ], limit=1)
            
            if not existing_commission:
                self.env['oig.commission'].create({
                    'customer_id': customer.id,
                    'agent_id': self.id,
                    'contribution_period_start': start_of_month,
                    'contribution_period_end': end_of_month,
                })

    def process_commissions_button(self):
        self.process_commissions()
