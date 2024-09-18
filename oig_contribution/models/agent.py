from odoo import models, fields, api

class OigAgent(models.Model):
    _name = 'oig.agent'
    _description = 'OIG Agent'

    name = fields.Char('Name', required=True)
    phone = fields.Char('Phone Number')
    email = fields.Char('Email')
    region_id = fields.Many2one('oig.region', string='Region', required=True)
    agent_id = fields.Char(string='Agent ID', readonly=True, required=True, copy=False, default='New')
    customer_ids = fields.One2many('oig.customer', 'agent_id', string='Customers Managed')
    image = fields.Binary('Image')
    total_customers = fields.Integer(compute='_compute_total_customers')

    @api.depends('customer_ids')
    def _compute_total_customers(self):
        for record in self:
            record.total_customers = len(record.customer_ids)

    @api.model
    def create(self, vals):
        if vals.get('agent_id', 'New') == 'New':
            vals['agent_id'] = self.env['ir.sequence'].next_by_code('oig.agent') or 'New'
        return super(OigAgent, self).create(vals)

