from odoo import models, fields, api
from datetime import date, timedelta  # Make sure to import these

class OigCustomer(models.Model):
    _name = 'oig.customer'
    _description = 'OIG Customer'

    name = fields.Char('Name', required=True)
    phone = fields.Char('Phone Number')
    email = fields.Char('Email')
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent')
    daily_contribution_amount = fields.Float('Daily Contribution Amount', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    contributions_ids = fields.One2many('oig.contribution', 'customer_id', string='Contributions')
    
    # Field to store the auto-generated customer ID
    customer_id = fields.Char(string='Customer ID', readonly=True, required=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('customer_id', 'New') == 'New':
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('oig.customer') or 'New'
        return super(OigCustomer, self).create(vals)
    
    def process_commissions(self):
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        existing_commission = self.env['oig.commission'].search([
            ('customer_id', '=', self.id),
            ('contribution_period_start', '=', start_of_month),
            ('contribution_period_end', '=', end_of_month),
        ], limit=1)
        
        if not existing_commission:
            self.env['oig.commission'].create({
                'customer_id': self.id,
                'agent_id': self.agent_id.id,
                'contribution_period_start': start_of_month,
                'contribution_period_end': end_of_month,
            })
    
    def process_commissions_button(self):
        self.process_commissions()
