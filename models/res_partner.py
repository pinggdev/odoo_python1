from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    #jika sebuah class tidak mempunyai "_name", maka kita tidak membuat sebuah tabel baru atau model baru pada database

    # inherit ini akan menambahkan field field yang ada didalam model yang lama

    is_pegawainya = fields.Boolean(string='Pegawai', default=False)
    is_customernya = fields.Boolean(string='Customer', default=False)
    
    