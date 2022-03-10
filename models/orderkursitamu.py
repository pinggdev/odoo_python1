from odoo import api, fields, models


class OrderKursiTamu(models.Model):
    _name = 'wedding.orderkursitamu'
    _description = 'New Description'

    name = fields.Char(string='Name')
