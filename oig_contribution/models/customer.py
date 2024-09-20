from odoo import models, fields, api

class OigCustomer(models.Model):
    _inherit = 'res.partner'  # We extend the existing res.partner model, which Odoo uses for customers

    agent_id = fields.Many2one('oig.agent', string='Assigned Agent', required=True)  # Each customer is assigned to an agent
    region_id = fields.Many2one('oig.region', string='Region', required=True)  # Assign a region to the customer
    customer_id = fields.Char(string='Customer ID', readonly=True, required=True, copy=False, default='New')  # Auto-generated customer ID

    # Overriding the create method to auto-generate customer ID using a sequence
    @api.model
    def create(self, vals):
        if vals.get('customer_id', 'New') == 'New':
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('oig.customer') or 'New'
        return super(OigCustomer, self).create(vals)
