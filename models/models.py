# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product Inherit'

    product_warranty = fields.Text(string="Product Warranty Code", readonly=True, compute='create_product_warranty')
    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')

    @api.depends('date_to', 'date_from')
    def create_product_warranty(self):
        for rec in self:
            date_to = rec.date_to
            date_from = rec.date_from
            if date_from and date_to:
                date_to = date_to.strftime('%d%m%-y')
                date_from = date_from.strftime('%d%m%-y')
                rec.product_warranty = 'PWR/' + str(date_to) + '/' + str(date_from)
                rec.check_valid_date = True
            else:
                rec.check_valid_date = False
                rec.product_warranty = ''

    @api.constrains('date_to', 'date_from')
    def check_date(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from < rec.date_to:
                    raise ValidationError('Date Start Warranty is smaller than Date Stop Warranty.')
