from odoo import models, fields

class OigRegion(models.Model):
    _name = 'oig.region'
    _description = 'OIG Region'

    name = fields.Char(string='Region Name', required=True)
    description = fields.Text(string='Description')
