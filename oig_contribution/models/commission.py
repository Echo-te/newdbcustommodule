from odoo import models, fields, api

class OigCommission(models.Model):
    _name = 'oig.commission'
    _description = 'Commission Management'
    _rec_name = 'name'

    name = fields.Char(string='Commission Reference', required=True, copy=False, readonly=True, default='New')
    agent_id = fields.Many2one('oig.agent', string='Agent', required=True, ondelete='cascade')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='cascade')
    contribution_id = fields.Many2one('oig.contribution', string='Contribution', required=True)
    region_id = fields.Many2one('oig.region', string='Region')
    amount = fields.Float(string='Commission Amount', required=True)
    income_account_id = fields.Many2one('account.account', string='Income Account', required=True)
    commission_date = fields.Date(string='Commission Date', default=fields.Date.context_today)

    @api.model
    def create(self, vals):
        # Automatically generate a commission reference ID
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('oig.commission') or 'New'
        return super(OigCommission, self).create(vals)

    @api.model
    def process_commissions(self, contribution):
        """
        This method processes the commission for a specific contribution.
        Called when processing commissions manually or through scheduled action.
        """
        commission_rate = 0.1  # Assuming 10% commission rate
        for line in contribution.contribution_line_ids:
            if line.status == 'paid':
                # Calculate the commission amount based on the contribution
                commission_amount = line.amount * commission_rate
                self.create({
                    'agent_id': contribution.agent_id.id,
                    'customer_id': contribution.customer_id.id,
                    'contribution_id': contribution.id,
                    'region_id': contribution.region_id.id,
                    'amount': commission_amount,
                    'income_account_id': contribution.agent_id.income_account_id.id,
                })

class OigContribution(models.Model):
    _inherit = 'oig.contribution'

    commission_ids = fields.One2many('oig.commission', 'contribution_id', string='Commissions')

class OigAgent(models.Model):
    _inherit = 'oig.agent'

    commission_ids = fields.One2many('oig.commission', 'agent_id', string='Commissions')
    income_account_id = fields.Many2one('account.account', string='Income Account', required=True)
