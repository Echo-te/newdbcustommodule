# models/agent.py
from odoo import models, fields

class OigAgent(models.Model):
    _name = 'oig.agent'
    _description = 'OIG Agent'

    name = fields.Char('Name', required=True)
    location = fields.Char('Location')
    customer_ids = fields.One2many('oig.customer', 'agent_id', string='Customers Managed')
    daily_collections_ids = fields.One2many('oig.contribution', 'agent_id', string='Daily Collections')
