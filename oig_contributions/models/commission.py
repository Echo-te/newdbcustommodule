from odoo import models, fields, api

class OIGCommission(models.Model):
    _name = 'oig.commission'
    _description = 'OIG Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    service_id = fields.Many2one('oig.service', string='Service', required=True, tracking=True)
    agent_id = fields.Many2one('oig.agent', string='Agent', required=True, tracking=True)
    amount = fields.Float(string='Commission Amount', required=True, tracking=True)
    date = fields.Date(string='Commission Date', required=True, tracking=True)
    account_id = fields.Many2one('account.account', string='Income Account', tracking=True)