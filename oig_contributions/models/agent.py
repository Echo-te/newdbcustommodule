from odoo import models, fields, api

class OIGAgent(models.Model):
    _name = 'oig.agent'
    _description = 'OIG Agent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    agent_code = fields.Char(string='Agent ID', readonly=True, copy=False, default='New', tracking=True)
    phone = fields.Char(string='Phone Number', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    region_id = fields.Many2one('oig.region', string='Region', tracking=True)
    customer_count = fields.Integer(compute='_compute_customer_count', string='Total Customers')
    image = fields.Image(string='Agent Picture')
    
    @api.model
    def create(self, vals):
        if vals.get('agent_code', 'New') == 'New':
            vals['agent_code'] = self.env['ir.sequence'].next_by_code('oig.agent.sequence') or 'New'
        return super(OIGAgent, self).create(vals)

    def _compute_customer_count(self):
        for agent in self:
            agent.customer_count = self.env['res.partner'].search_count([('agent_id', '=', agent.id)])

    def action_view_customers(self):
        self.ensure_one()
        return {
            'name': 'Customers',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'domain': [('agent_id', '=', self.id)],
        }