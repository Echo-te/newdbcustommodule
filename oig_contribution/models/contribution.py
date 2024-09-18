from odoo import models, fields, api

class OigContribution(models.Model):
    _name = 'oig.contribution'
    _description = 'OIG Contribution'

    service_id = fields.Many2one('oig.service', string='Service', required=True)
    day = fields.Integer(string='Day', required=True)
    amount = fields.Float(string='Amount', default=500)
    contribution_date = fields.Date(string='Contribution Date', required=True)
    status = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')], string='Status', default='pending')

    @api.model
    def create(self, vals):
        # Overpayment handling: Adjust the remaining balance to next day's contribution
        service = self.env['oig.service'].browse(vals.get('service_id'))
        if vals.get('amount') > service.agreed_amount:
            excess_amount = vals['amount'] - service.agreed_amount
            vals['amount'] = service.agreed_amount
            self.env['oig.contribution'].create({
                'service_id': service.id,
                'day': vals.get('day') + 1,
                'amount': excess_amount,
                'contribution_date': fields.Date.today(),
                'status': 'pending',
            })
        return super(OigContribution, self).create(vals)
