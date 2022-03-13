from odoo import api, fields, models


class Order(models.Model):
    _name = 'wedding.order'
    _description = 'New Description'

    orderpanggungdetail_ids = fields.One2many(
        comodel_name='wedding.orderpanggungdetail', 
        inverse_name='order_id', 
        string='Order Detail')
    
    orderkursitamudetail_ids = fields.One2many(
        comodel_name='wedding.orderkursitamudetail', 
        inverse_name='orderk_id', 
        string='Order Kursi Tamu')
    
    
    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    tanggal_pengiriman = fields.Date(string='Tanggal Pengiriman', default=fields.Date.today())
    
    total = fields.Integer(compute='_compute_total', string='Total', store=True)
    
    @api.depends('orderpanggungdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['wedding.orderpanggungdetail'].search([('order_id', '=', record.id)]).mapped('harga'))
            b = sum(self.env['wedding.orderkursitamudetail'].search([('orderk_id', '=', record.id)]).mapped('harga'))
            record.total = a + b
    

class OrderPanggungDetail(models.Model):
    _name = 'wedding.orderpanggungdetail'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='wedding.order', string='Order')
    panggung_id = fields.Many2one(comodel_name='wedding.panggung', string='Panggung')   
    
         
    name = fields.Char(string='Name')
    harga = fields.Integer(compute='_compute_harga', string='harga')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='harga_satuan')
    
    @api.depends('panggung_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.panggung_id.harga
    
    
    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
           record.harga = record.harga_satuan * record.qty
           
    @api.model
    def create(self,vals):
        record = super(OrderPanggungDetail, self).create(vals) 
        if record.qty:
            self.env['wedding.panggung'].search([('id','=',record.panggung_id.id)]).write({'stok':record.panggung_id.stok-record.qty})
            return record
        
class OrderKursiTamuDetail(models.Model):
    _name = 'wedding.orderkursitamudetail'
    _description = 'New Description'
    
    orderk_id = fields.Many2one(comodel_name='wedding.order', string='Order Kursi')
    kursitamu_id = fields.Many2one(comodel_name='wedding.kursitamu', string='Kursi Tamu')
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='harga_satuan')
    
    @api.depends('kursitamu_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.kursitamu_id.harga
    
    qty = fields.Integer(string='Quantity')
    
    harga = fields.Integer(compute='_compute_harga', string='harga')
    
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
               record.harga = record.harga_satuan * record.qty
    
    
    