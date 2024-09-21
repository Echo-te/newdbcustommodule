from odoo import models, fields, api

class OIGCustomer(models.Model):
    _inherit = 'res.partner'

    is_oig_customer = fields.Boolean(string='Is OIG Customer', default=False)
    customer_code = fields.Char(string='Customer ID', readonly=True, copy=False, default='New')
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent')
    region_id = fields.Many2one('oig.region', string='Region')

    @api.model
    def create(self, vals):
        if vals.get('is_oig_customer', False) and vals.get('customer_code', 'New') == 'New':
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('oig.customer.sequence') or 'New'
        return super(OIGCustomer, self).create(vals)