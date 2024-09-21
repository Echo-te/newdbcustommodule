from odoo import models, fields, api
from datetime import timedelta

class OIGService(models.Model):
    _name = 'oig.service'
    _description = 'OIG Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    agent_id = fields.Many2one('oig.agent', string='Assigned Agent', tracking=True)
    agreed_amount = fields.Float(string='Agreed Contribution Amount', required=True, tracking=True)
    phone = fields.Char(related='customer_id.phone', string='Customer Phone', readonly=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)
    duration = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)
    creation_date = fields.Date(string='Service Creation Date', default=fields.Date.today, tracking=True)
    contribution_line_ids = fields.One2many('oig.contribution.line', 'service_id', string='Contributions')
    total_contributed = fields.Float(string='Total Contributed', compute='_compute_total_contributed', store=True)
    current_days = fields.Integer(string='Current Days', compute='_compute_current_days', store=True)
    region_id = fields.Many2one(related='customer_id.region_id', string='Region', store=True)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for service in self:
            if service.start_date and service.end_date:
                service.duration = (service.end_date - service.start_date).days + 1
            else:
                service.duration = 0

    @api.depends('contribution_line_ids.amount', 'contribution_line_ids.state')
    def _compute_total_contributed(self):
        for service in self:
            service.total_contributed = sum(line.amount for line in service.contribution_line_ids if line.state == 'paid')

    @api.depends('contribution_line_ids.state')
    def _compute_current_days(self):
        for service in self:
            service.current_days = len(service.contribution_line_ids.filtered(lambda l: l.state == 'paid'))

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            self.agent_id = self.customer_id.agent_id

    def action_process_commission(self):
        for service in self:
            commission_amount = service.agreed_amount * service.current_days
            self.env['oig.commission'].create({
                'service_id': service.id,
                'agent_id': service.agent_id.id,
                'amount': commission_amount,
                'date': fields.Date.today(),
            })
            # Deduct commission from contributions
            remaining_commission = commission_amount
            for line in service.contribution_line_ids.filtered(lambda l: l.state == 'paid'):
                if remaining_commission <= 0:
                    break
                if line.amount <= remaining_commission:
                    remaining_commission -= line.amount
                    line.amount = 0
                else:
                    line.amount -= remaining_commission
                    remaining_commission = 0
            service._compute_total_contributed()