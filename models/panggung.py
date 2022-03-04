from odoo import api, fields, models


class Panggung(models.Model):
    _name = 'wedding.panggung'
    _description = 'New Description'

    name = fields.Char(string='Name', required=True)
    pelaminan = fields.Many2one(comodel_name='wedding.pelaminan', string='Tipe Pelaminan', required=True, 
    domain=[('harga','>', '900000')]
    )
    
    bunga = fields.Selection(string='Tipe Bunga', selection=[('bunga mati', 'Bunga Mati'), ('bunga hidup', 'Bunga Hidup')])
    accesories = fields.Char(string='Accesories Pelaminan')
    harga = fields.Char(compute='_compute_harga', string='Harga')
    
    @api.depends('pelaminan')
    def _compute_harga(self):
        for record in self:
            record.harga = record.pelaminan.harga + 200000
        
    