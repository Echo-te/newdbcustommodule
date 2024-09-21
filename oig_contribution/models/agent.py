from odoo import models, fields, api

class OigAgent(models.Model):
    _name = 'oig.agent'
    _description = 'Agent Management'

    name = fields.Char(string='Agent Name', required=True)
    agent_id = fields.Char(string='Agent ID', readonly=True, required=True, copy=False, default='New')
    customer_ids = fields.One2many('res.partner', 'agent_id', string='Assigned Customers')
    region_id = fields.Many2one('oig.region', string='Region', required=True)
    performance_score = fields.Float(string='Performance Score', compute='_compute_performance_score', store=True)

    @api.model
    def create(self, vals):
        if vals.get('agent_id', 'New') == 'New':
            vals['agent_id'] = self.env['ir.sequence'].next_by_code('oig.agent') or 'New'
        return super(OigAgent, self).create(vals)
