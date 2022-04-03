from multiprocessing.sharedctypes import Value
from odoo import http, fields, models
from odoo.http import request
import json

class KursiTamuCon(http.Controller):
    @http.route(['/kursitamu','/kursitamu/<int:idnya>'], auth='public', methods=['GET'], csrf=True)
    def getKursiTamu(self, idnya=None, **kwargs):
        value = []
        if not idnya:
            kursi = request.env['wedding.kursitamu'].search([])
            for k in kursi:
                value.append({
                    "id"            : k.id,
                    "namakursi"     : k.name,
                    "tipe_bahan"    : k.tipe,
                    "stok_tersedia" : k.stok,
                    "harga_sewa"    : k.harga
                })
            # data dimasukkan kedalam sebuah list, yaitu value(variable)
            return json.dumps(value)
        else:
            kursiid = request.env['wedding.kursitamu'].search([('id', '=', idnya)])
            for k in kursiid:
                value.append({
                    "id"            : k.id,
                    "namakursi"     : k.name,
                    "tipe_bahan"    : k.tipe,
                    "stok_tersedia" : k.stok,
                    "harga_sewa"    : k.harga
                })
            # data dimasukkan kedalam sebuah list, yaitu value(variable)
            return json.dumps(value)

    @http.route('/createkursi', auth='user', type='json', methods=['POST'])
    def createKursi(self, **kw):
        if request.jsonrequest:
            if kw['name']:
                vals = {
                    'name'  : kw['name'],
                    'tipe'  : kw['tipe'],
                    'stok'  : kw['stok'],
                    'harga' : kw['harga'],
                }
                kursiBaru = request.env['wedding.kursitamu'].create(vals)
                args = {
                    'success'   : True,
                    'ID'        : kursiBaru.id 
                    }
                return args