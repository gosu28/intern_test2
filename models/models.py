# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product Inherit'

    product_warranty = fields.Text(string="Product Warranty Code", readonly=True, compute='create_product_warranty')
    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')
    time_interval = fields.Text(string="Time Interval", compute='check_date_stop_warranty')
    check_valid_date = fields.Boolean(string='Check Valid')

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

    @api.depends('date_from')
    def check_date_stop_warranty(self):
        current_date = date.today()
        for rec in self:
            count_days = ''
            if rec.date_from:
                if current_date < rec.date_from:
                    delta = rec.date_from - current_date
                    if delta.days >= 365:
                        if (delta.days // 365) == 1:
                            count_days = str(delta.days // 365) + ' year'
                        else:
                            count_days = str(delta.days // 365) + ' years'
                    elif delta.days >= 30:
                        if (delta.days // 30) == 1:
                            count_days = str(delta.days // 30) + ' month'
                        else:
                            count_days = str(delta.days // 30) + ' months'
                    elif delta.days == 1:
                        count_days = str(delta.days) + ' day'
                    else:
                        count_days = str(delta.days) + ' days'
            rec.time_interval = count_days


class SaleOder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit'

    discount_with_warranty = fields.Monetary(string='Estimated Discount Total With Product Warranty', readonly=True,
                                             store=True, compute='discount_total_with_warranty')

    @api.depends('order_line')
    def discount_total_with_warranty(self):
        for rec in self:
            estimated_total = 0.0
            for line in rec.order_line:
                estimated_total += line.product_price
        rec.update({
            'discount_with_warranty': estimated_total
        })


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_price = fields.Monetary(string='Product Price', compute='calculate_price')

    @api.onchange('price_subtotal')
    def calculate_price(self):
        for order in self:
            if order.product_id:
                if not order.product_id.product_warranty:
                    order.product_price = order.price_subtotal * 0.9
                else:
                    order.product_price = order.price_subtotal
