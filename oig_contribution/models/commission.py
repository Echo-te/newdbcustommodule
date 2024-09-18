from odoo import models, fields, api

class OigCommission(models.Model):
    _name = 'oig.commission'
    _description = 'OIG Commission'

    agent_id = fields.Many2one('oig.agent', string='Agent', required=True)
    service_id = fields.Many2one('oig.service', string='Service', required=True)
    commission_amount = fields.Float(string='Commission Amount', required=True)
    income_account_id = fields.Many2one('account.account', string='Income Account')
