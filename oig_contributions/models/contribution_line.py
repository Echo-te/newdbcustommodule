from odoo import models, fields, api

class OIGContributionLine(models.Model):
    _name = 'oig.contribution.line'
    _description = 'OIG Contribution Line'

    service_id = fields.Many2one('oig.service', string='Service', required=True)
    day = fields.Integer(string='Day')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Contribution Date')
    state = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')], string='Status', default='pending')