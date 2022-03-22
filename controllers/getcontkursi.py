from odoo import http, fields, models
from odoo.http import request
import json

class KursiTamuCon(http.Controller):
    @http.route('/kursitamu', auth='public', methods=['GET'])
    def getKursiTamu(self, **kwargs):
        kursi = request.env['wedding.kursitamu'].search([])
        value = []
        for k in kursi:
            value.append({
                "namakursi"     : k.name,
                "tipe_bahan"    : k.tipe,
                "stok_tersedia" : k.stok,
                "harga_sewa"    : k.harga
            })
        # data dimasukkan kedalam sebuah list, yaitu value(variable)
        return json.dumps(value)