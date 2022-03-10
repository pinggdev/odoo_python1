from odoo import api, fields, models


class Order(models.Model):
    _name = 'wedding.order'
    _description = 'New Description'
    
    orderdetail_ids = fields.One2many(comodel_name='wedding.order_detail', inverse_name='order_id', string='Order Detail')
    
    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pesan', default=fields.Datetime.now())
    total = fields.Integer(compute='_compute_total', string='Total', store=True)
    
    @api.depends('orderdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['wedding.order_detail'].search([('order_id', '=', record.id)]).mapped('harga'))
            record.total = a
    # self in gunanyan untuk mengambil tabel dari model lain


class OrderDetail(models.Model):
    _name = 'wedding.order_detail'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='wedding.order', string='Order')
    panggung_id = fields.Many2one(comodel_name='wedding.panggung', string='Panggung')
    

    name = fields.Selection(string='Name', selection=[('panggung', 'Panggung'), ('kursi tamu', 'Kursi Tamu')])
    harga = fields.Integer(compute='_compute_harga', string='harga')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='harga_satuan')
    
    @api.depends('panggung_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.panggung_id.harga
    
    @api.depends('qty', 'harga_satuan')
    def _compute_harga(self):
        for record in self:
            record.harga = record.panggung_id.harga * record.qty

    @api.model
    def create(self, vals): 
        record = super(OrderDetail, self).create(vals)
        if record.qty:
            self.env['wedding.panggung'].search([('id', '=', record.panggung_id.id)]).write({'stok':record.panggung_id.stok-record.qty})
            return record