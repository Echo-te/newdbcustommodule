from odoo import models, fields

class OigRegion(models.Model):
    _name = 'oig.region'
    _description = 'OIG Region'

    name = fields.Char('Region Name', required=True)
