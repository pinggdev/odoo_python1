from odoo import api, fields, models


class Pengembalian(models.Model):
    _name = 'wedding.pengembalian'
    _description = 'Pengembalian Barang Sewa'

    name = fields.Char(string='Name')
    order_id = fields.Many2one(comodel_name='wedding.order', string='Order')

    nama_penyewa = fields.Char(compute='_compute_nama_penyewa', string='nama_penyewa')
    
    @api.depends('order_id')
    def _compute_nama_penyewa(self):
        for record in self:
            record.nama_penyewa = self.env['wedding.order'].search([('id', '=', record.order_id.id)]).mapped('pemesan')

    tgl_pengembalian = fields.Date(string='', default=fields.Date.today())

    tagihan = fields.Char(compute='_compute_tagihan', string='tagihan')
    
    @api.depends('order_id')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.order_id.total
    
    
    @api.model
    def create(self,vals):
        record = super(Pengembalian, self).create(vals) 
        if record.tgl_pengembalian:
            self.env['wedding.order'].search([('id','=',record.order_id.id)]).write({'sudah_kembali':True})
            return record