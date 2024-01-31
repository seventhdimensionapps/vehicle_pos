from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    location_src_id = fields.Many2one('stock.location', 'Source Location', required=True, copy=True, domain="[('usage','=','internal')]")
    van_no = fields.Many2one('stock.location', 'Van Number', required=True, copy=True, domain="[('is_van_location','=',True)]")

    @api.onchange('partner_id')
    def _onchange_partner_id_location(self):
        if self.partner_id:
            self.location_src_id = self.partner_id.location_src_id.id or False
            self.warehouse_id = self.partner_id.location_src_id.warehouse_id.id or False
