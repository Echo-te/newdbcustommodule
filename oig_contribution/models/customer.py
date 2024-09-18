from odoo import models, fields, api

class OigCustomer(models.Model):
    _inherit = 'res.partner'

    agent_id = fields.Many2one('oig.agent', string='Assigned Agent', required=True)
    region_id = fields.Many2one('oig.region', string='Region', required=True)
    customer_id = fields.Char(string='Customer ID', readonly=True, required=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('customer_id', 'New') == 'New':
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('oig.customer') or 'New'
        return super(OigCustomer, self).create(vals)
