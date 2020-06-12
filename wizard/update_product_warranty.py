from odoo import fields, models, api


class UpdateProductWarranty(models.TransientModel):
    _name = 'update.product.warranty'
    _description = 'Mass Update Product Warranty'

    product_warranty = fields.Text(string="Product Warranty Code", readonly=True, compute='update')
    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')

    @api.depends('date_to', 'date_from')
    def update(self):
        date_to = self.date_to
        date_from = self.date_from
        if date_from and date_to:
            date_to = date_to.strftime('%d%m%-y')
            date_from = date_from.strftime('%d%m%-y')
        else:
            self.product_warranty = ''
        list = self.env['product.product'].browse(self._context['active_ids'])
        for rec in list:
            rec.date_to = self.date_to
            rec.date_from = self.date_from
            rec.product_warranty = self.product_warranty
            if date_from and date_to:
                self.product_warranty = 'PWR/' + str(date_to) + '/' + str(date_from)
            else:
                self.product_warranty = ''
