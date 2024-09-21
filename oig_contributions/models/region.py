from odoo import models, fields

class OIGRegion(models.Model):
    _name = 'oig.region'
    _description = 'OIG Region'

    name = fields.Char(string='Region Name', required=True)