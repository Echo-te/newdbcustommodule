from odoo import api, fields, models

class OIGContribution(models.Model):
    _name = 'oig.contribution'
    _description = 'Customer Contribution'
    _order = 'contribution_date desc'

    service_id = fields.Many2one('oig.service', string='Service', required=True, ondelete='cascade')
    customer_id = fields.Many2one('res.partner', related='service_id.customer_id', string='Customer', readonly=True)
    agent_id = fields.Many2one('oig.agent', related='service_id.agent_id', string='Agent', readonly=True)
    day = fields.Integer(string='Day', required=True)
    amount = fields.Float(string='Amount', required=True)
    contribution_date = fields.Date(string='Contribution Date', required=True)
    status = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')], string='Status', default='pending', required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    @api.depends('amount')
    def _compute_total_amount(self):
        for contribution in self:
            contribution.total_amount = sum(line.amount for line in contribution.service_id.contribution_ids)

    @api.onchange('amount')
    def _onchange_amount(self):
        if self.amount > self.service_id.agreed_amount:
            overpayment = self.amount - self.service_id.agreed_amount
            self.handle_overpayment(self.service_id, overpayment)
            self.amount = self.service_id.agreed_amount  # Set the amount to agreed amount for the current day

    def handle_overpayment(self, service, overpayment_amount):
        """ Handle cases where contributions exceed the agreed amount, forwarding excess to the next days. """
        contributions = service.contribution_ids.filtered(lambda c: c.status == 'pending' and c.id != self.id).sorted('day')
        for contribution in contributions:
            if overpayment_amount <= 0:
                break
            # Apply the overpayment to the next pending contribution
            remaining_for_day = contribution.service_id.agreed_amount - contribution.amount
            if overpayment_amount <= remaining_for_day:
                contribution.amount += overpayment_amount
                overpayment_amount = 0
            else:
                contribution.amount = contribution.service_id.agreed_amount
                overpayment_amount -= remaining_for_day
            # Mark contribution as paid if fully covered
            if contribution.amount >= contribution.service_id.agreed_amount:
                contribution.status = 'paid'

    @api.model
    def create(self, vals):
        """ Override the create method to handle overpayment on contribution creation. """
        contribution = super(OIGContribution, self).create(vals)
        if contribution.amount > contribution.service_id.agreed_amount:
            overpayment = contribution.amount - contribution.service_id.agreed_amount
            contribution.handle_overpayment(contribution.service_id, overpayment)
            contribution.amount = contribution.service_id.agreed_amount
        return contribution
