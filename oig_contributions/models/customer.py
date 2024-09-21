from odoo import models, fields, api

class OIGCustomer(models.Model):
    _inherit = 'res.partner'
    
    customer_code = fields.Char(string='Customer ID', readonly=True, copy=False, default='New')
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent')
    region_id = fields.Many2one('oig.region', string='Region')
    
    # Add a computed field to identify customers
    is_customer = fields.Boolean(string='Is a Customer', compute='_compute_is_customer', store=True)
    
    @api.depends('company_type')
    def _compute_is_customer(self):
        for partner in self:
            partner.is_customer = partner.company_type == 'person'
    
    @api.model
    def create(self, vals):
        if vals.get('customer_code', 'New') == 'New':
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('oig.customer.sequence') or 'New'
        return super(OIGCustomer, self).create(vals)