from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.origin and 'S0' in res.origin:
            sale_id = res.env['sale.order'].search([('name','=',res.origin)])
            if res.picking_type_id and res.picking_type_id.code == 'internal':
                res.location_id = sale_id.location_src_id.id
                res.location_dest_id = sale_id.van_no.id
            elif res.picking_type_id and res.picking_type_id.code == 'outgoing':
                res.location_id = sale_id.van_no.id
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        if vals.get('origin', False) and 'S0' in vals.get('origin', ''):
            sale_id = self.env['sale.order'].search([('name','=',vals.get('origin', ''))])
            if vals.get('picking_type_id', False):
                picking_type_id = self.env['stock.picking.type'].search([('id','=',vals.get('picking_type_id', -1))])
                if picking_type_id and picking_type_id.code == 'internal':
                    vals['location_id'] = sale_id.location_src_id.id
                    vals['location_dest_id'] = sale_id.van_no.id
        res = super(StockMove, self).create(vals)
        return res


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_van_location = fields.Boolean()
