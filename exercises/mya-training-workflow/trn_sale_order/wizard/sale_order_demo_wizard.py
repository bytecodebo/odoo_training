import datetime
import logging
import random
import time
from datetime import datetime, date, timedelta
from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.addons.trn_main_setting.tools.fun_dates import fn_time_long
from odoo.exceptions import UserError
from odoo.tools import float_round

_logger = logging.getLogger(__name__)


class SaleOrderDemoWizard(models.TransientModel):
    _name = 'sale.order.demo.wizard'
    _description = 'Sale Order Demo Wizard'

    # @api.model
    # def _get_domain_sellers_orders(self):
    #     company_id = self.company_id or self.env.company
    #     user_field_type = self.env.context.get('user_field_type', 'is_a_salesman')
    #     domain = []
    #     domain_user = [('company_id', 'in', [False, company_id.id])]
    #     if user_field_type:
    #         domain_user += [(user_field_type, '=', True)]
    #     user_ids = self.env['res.users'].search(domain_user)
    #     if user_ids:
    #         domain = "[('id', 'in', %s)]" % user_ids.ids
    #     return domain

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    test_max_prd = fields.Integer(string="Max items per Sale", default=1)
    test_max_orders = fields.Integer(string="Max orders", default=50)
    test_qty_orders = fields.Integer(string="Max orders", default=10)
    test_max_invoice = fields.Integer(string="Max Invoice per Package", default=50)
    test_draft_orders = fields.Boolean(default=True, string="Draft orders")
    test_sale_orders = fields.Boolean(default=True, string="Confirm orders")
    test_done_orders = fields.Boolean(default=False, string="Block orders")
    test_draft_invoice = fields.Boolean(default=False)
    test_public_invoice = fields.Boolean(default=False)
    user_ids = fields.Many2many('res.users')
    start_event = fields.Datetime(string="Start from", copy=False, default=datetime.now().replace(day=1, hour=4))
    end_event = fields.Datetime(string="End to", copy=False,
                                default=(datetime.now() + timedelta(days=1)).replace(hour=19))
    test_qty_invoice = fields.Integer(string="Number of Invoices", default=10)
    test_save_interval = fields.Integer(string="# Confirmation Interval", default=50)
    test_start_time = fields.Float(string="Start time (HH:mm)", default=8)
    test_end_time = fields.Float(string="End time (HH:mm)", default=18.5)
    test_exclude_holidays = fields.Boolean(default=True)
    test_max_orders_per_day = fields.Integer(default=1)
    test_interval_orders_per_day = fields.Integer(default=1)
    sale_order_type = fields.Many2one('sale.order.type')
    test_order_type_id = fields.Many2one('sale.order.type', domain="[('company_id', 'in', [False, company_id])]")

    @api.onchange('start_event')
    def _onchange_start_event(self):
        if self.start_event:
            end_event = self.start_event
            current_date = fields.Datetime.now()
            if current_date.date().month == end_event.date().month:
                self.end_event = current_date - timedelta(days=1)
            else:
                self.end_event = (end_event + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    def create_invoices(self):
        pass

    def action_process_options_old(self):

        max_index = self.test_qty_orders
        qty_users = len(self.user_ids) * max_index + int(max_index/2)
        partner_ids, product_ids = self._get_data_for_testing(qty=qty_users)
        user_cashier_ids = self.user_ids
        remaining_qty = max_index
        interval_save = self.test_save_interval if self.test_qty_invoice > 50 else self.test_qty_invoice
        commit_intervals = self._get_intervals(remaining_qty, interval_save)
        factor = 1.2
        if remaining_qty <= 10:
            factor = 1.5
        elif remaining_qty <= 30:
            factor = 1.6
        elif remaining_qty <= 50:
            factor = 1.7
        elif remaining_qty <= 200:
            factor = 1.8
        start_index = 0
        if not partner_ids:
            raise UserError(_(""""There is no client enabled to generate sale orders. Verify that the following data:
                                               - Code
                                               - Document Type
                                               - NIT/IC
                                               - NIT/IC validation"""))

        vals_partners = []
        vals_partners += self._get_random_values(partner_ids.ids, remaining_qty)

        vals_user_cashiers = self._get_random_values(user_cashier_ids.ids, remaining_qty)

        start_event = self.start_event.date()
        start_time = self.test_start_time
        date_time = self._get_date_time_order(start_event, start_time)
        # time_vals = {
        #    'order_qty': self.test_qty_orders}
        # date_time_intervals = self._get_period_date_orders(**time_vals)
        # order_ids = self.env['sale.order']
        start_index = 0
        # job_orders = []
        # predefine = self._get_predefine_header()
        # for inv in range(0, max_index):
        #     kwargs = predefine
        #     date_time = date_time_intervals[inv]['date_order']
        #     prd_qty_rand = self._get_max_doc_lines_random(minimo=1, maximo=self.test_max_prd)
        #     vals_products =self._get_random_values(product_ids.ids, prd_qty_rand, model='product')
        #     user_cashier_id = user_cashier_ids.filtered(lambda p: p.id == vals_user_cashiers[inv])
        #     customer_id = partner_ids.filtered(lambda p: p.id == vals_partners[inv])
        #     # partner_ids -=customer_id
        #     kwargs.update({
        #         'partner_id': customer_id.id,
        #         'business_name': customer_id.name.upper(),
        #         'vat': customer_id.vat,
        #         'user_id': user_cashier_id.id,
        #         'create_date': date_time,
        #         'date_order': date_time
        #     })
        #     order_vals = self._prepare_sale_order(**kwargs)
        #     order_vals.update(predefine)
        #     detail = []
        #     for prd in product_ids.filtered(lambda x: x.id in vals_products):
        #         qty_rand = self._get_max_qty_product_random()
        #         price_unit = self._get_max_price_unit_random()
        #         discount = 0.0
        #         prd_vals = {'product_id': prd.id,
        #                     'product_name': prd.name,
        #                     'price_unit': price_unit,
        #                     'product_uom_qty': qty_rand if prd.type != 'service' else 1,
        #                     'company_id': self.company_id.id}
        #         line_vals = self._prepare_order_lines(**prd_vals)
        #         # detail.append(line_vals)
        #         # -print('----->>>>\n\n lines_prd::->', line_vals)
        #         detail.append(line_vals)
        #
        #     order_vals['order_line'] = [(0, 0, line) for line in detail]
        #     time.sleep(0.1)
        #     job_orders.append(order_vals)
        #     # _logger.info("\n\n Order Nro: %s \n\n" % order_vals)
        #     # sale_order_lines.append(order)
        # max_result = 30
        # index_so = int(len(job_orders) / max_result)
        # priority = 4
        # for x in range(0, index_so):
        #     order_values = job_orders[start_index:start_index+max_result]
        #     if not order_values:
        #         continue
        #     start_index += max_result
        #     self.with_delay(priority=priority, description="Proceso masivo de reg. de pedidos", eta=10).action_generate_batch_orders(order_values, date_time)
        #     priority += 2

    def action_process_options(self):
        priority = 10
        self.with_delay(priority=priority, description="Start proceso masivo de reg. de pedidos",
                        eta=10)._process_queue_jobs()
        return True

    def _process_queue_jobs(self, after_to=30):
        remaining_qty = self.test_qty_orders
        start_event = self.start_event.date()
        start_time = self.test_start_time
        date_time = self._get_date_time_order(start_event, start_time)
        interval_save = self.test_save_interval if self.test_qty_invoice > 50 else self.test_qty_invoice
        commit_intervals = self._get_intervals(remaining_qty, interval_save)
        params = {'ctx_own_prd_price': False}
        factor = 1.2
        if remaining_qty <= 10:
            factor = 1.5
        elif remaining_qty <= 30:
            factor = 1.6
        elif remaining_qty <= 50:
            factor = 1.7
        elif remaining_qty <= 200:
            factor = 1.8
        limit = int(remaining_qty * factor)
        order_vals = self.get_lazy_random_orders(remaining_qty, limit=limit, **params)
        order_ids = []
        priority = 10
        for order in order_vals:
            order_ids.append(order)
            if len(order_ids) >= 50:
                self.with_delay(priority=priority, description="Proceso masivo de reg. de pedidos",
                                eta=after_to).action_generate_batch_orders(order_ids, date_time)
                order_ids = []
                priority += 2
        if order_ids:
            self.with_delay(priority=priority, description="Proceso masivo de reg. de pedidos",
                            eta=after_to).action_generate_batch_orders(order_ids, date_time)

    def get_lazy_random_orders(self,qty=1, limit=10,**kwargs):
        yield from self._get_random_orders(qty=qty, limit=limit, **kwargs)

    def _get_random_orders(self, qty=1, limit=10, **kwargs):
        max_index = qty
        predefine = self._get_predefine_header()
        if not kwargs:
            kwargs = {}
        ctx = dict(self.env.context)
        ctx.update(**kwargs)
        max_index = self.test_qty_orders
        qty_users = len(self.user_ids) * max_index + int(max_index / 2)
        partner_ids, product_ids = self._get_data_for_testing(qty=qty_users)
        user_cashier_ids = self.user_ids
        remaining_qty = max_index
        vals_partners = []
        vals_partners += self._get_random_values(partner_ids.ids, remaining_qty)

        vals_user_cashiers = self._get_random_values(user_cashier_ids.ids, remaining_qty)
        time_vals = {
            'order_qty': self.test_qty_orders
        }
        date_time_intervals = self._get_period_date_orders(**time_vals)
        order_values = []
        for inv in range(0, max_index):
            kwargs = predefine
            date_time = date_time_intervals[inv]['date_order']
            prd_qty_rand = self._get_max_doc_lines_random(minimo=1, maximo=self.test_max_prd)
            vals_products =self._get_random_values(product_ids.ids, prd_qty_rand, model='product')
            user_cashier_id = user_cashier_ids.filtered(lambda p: p.id == vals_user_cashiers[inv])
            customer_id = partner_ids.filtered(lambda p: p.id == vals_partners[inv])
            # partner_ids -=customer_id
            kwargs.update({
                'partner_id': customer_id.id,
                'business_name': customer_id.name.upper(),
                'vat': customer_id.vat,
                'user_id': user_cashier_id.id,
                'create_date': date_time,
                'date_order': date_time
            })
            order_vals = self._prepare_sale_order(**kwargs)
            order_vals.update(predefine)
            detail = []
            for prd in product_ids.filtered(lambda x: x.id in vals_products):
                qty_rand = self._get_max_qty_product_random()
                price_unit = self._get_max_price_unit_random()
                discount = 0.0
                prd_vals = {'product_id': prd.id,
                            'product_name': prd.name,
                            'price_unit': price_unit,
                            'product_uom_qty': qty_rand if prd.type != 'service' else 1,
                            'company_id': self.company_id.id}
                line_vals = self._prepare_order_lines(**prd_vals)
                # detail.append(line_vals)
                # -print('----->>>>\n\n lines_prd::->', line_vals)
                detail.append(line_vals)

            order_vals['order_line'] = [(0, 0, line) for line in detail]
            time.sleep(0.1)
            order_values.append(order_vals)
        return order_values

    def action_generate_batch_orders(self, order_values, date_time):
        order_ids = self.env['sale.order'].sudo().create(order_values)
        # order.create_date = date_time
        # order.write({'create_date': date_time})
        # order.update({'create_date': date_time})
        # _logger.info("\n\n Order Nro: %s  %s %s %s\n\n" % (order.id, order.name, inv, date_time))
        # order_ids |= order
        if self.test_sale_orders:
            for order in order_ids:
                order.action_confirm()
                order.date_order = date_time
                order.write({'date_order': date_time})
                order.update({'date_order': date_time})
                sql_query = "update sale_order set create_date=date_order where id=%s" % order.id or order._origin.id
                try:
                    self.env.cr.execute(sql_query)
                except Exception as e:
                    # -print(e)
                    pass
                self.compute_specific_process(order)

    def _get_intervals(self, qty, interval):
        intervals = []
        index = 0
        while index < qty:
            if index + interval >= qty:
                intervals.append(qty)
            else:
                intervals.append(index + interval)
            index += interval
        return intervals

    def _get_date_time_order(self, order_date, order_time, order_end_date=None, order_end_time=None):
        date_time = fn_time_long(order_date, order_time, self.env.user.tz)
        if not order_end_date:
            order_end_date = self.end_event.date()
        if not order_end_time:
            order_end_time = self.test_end_time

        if date_time.weekday == 6:
            date_time = date_time + timedelta(days=1)
        # TODO Check for holidays

        return date_time

    def _get_predefine_header(self):
        return {
            'company_id': self.company_id.id,
            'type_id': self.test_order_type_id.id,
            'state': 'draft',
         }

    def compute_specific_process(self, order, **kwargs):
        pass

    def _process_invoice_moves(self, move_ids):
        pass

    def _apply_more_discounts(self, move):
        pass

    def _get_intervals(self, qty, interval):
        intervals = []
        index = 0
        while index < qty:
            if index + interval >= qty:
                intervals.append(qty)
            else:
                intervals.append(index + interval)
            index += interval
        return intervals

    def _get_time_intervals(self, start_time, end_time, interval=0.20):
        intervals = []
        while start_time < end_time:
            intervals.append(start_time)
            start_time += interval
            start_time = round(start_time,2)
        return intervals

    def _apply_functions_after_post(self, move):
        pass

    def _get_data_for_testing(self, qty=10):
        # Obteniendo partners
        domain_partner = self._get_domain_customers_random()

        # Obteniendo productos
        domain_products = self._get_domain_products_random()

        partner_ids = self.env['res.partner'].search(domain_partner, limit=qty)
        product_ids = self.env['product.template'].search(domain_products, limit=500)
        return partner_ids, product_ids

    def action_test_period(self):
        kwargs = {
            'order_qty': self.test_qty_orders
        }
        self._get_period_date_orders(**kwargs)

    def _get_period_date_orders(self, **kwargs):
        max_orders_day = kwargs.get('max_orders', self.test_max_orders_per_day)
        interval_orders = kwargs.get('interval_orders', self.test_interval_orders_per_day)
        # date_time = tcp_timeLong(order_date, order_time, self.env.user.tz)
        tz = self.user_ids[0].partner_id.tz or self.env.user.partner_id.tz
        order_start_date = kwargs.get('order_start_date', self.start_event)
        order_start_time = kwargs.get('order_start_time', self.test_start_time)
        order_qty = kwargs.get('order_qty', self.test_qty_orders)
        order_end_date = kwargs.get('order_end_date', self.end_event)
        order_end_time = kwargs.get('order_end_time', self.test_end_time)
        interval_start = fn_time_long(order_start_date, order_start_time,tz_str=tz)
        interval_end = fn_time_long(order_end_date, order_end_time, tz_str=tz)

        stop_order = False
        index_date = order_start_date
        index_qty = 0
        order_date_vals = []

        if index_date.weekday == 6:
            index_date = (order_start_date + timedelta(days=1))
        interval_days = []
        interval_date_start = interval_start.date()
        interval_date_end = interval_end.date()
        while interval_date_start <= interval_date_end:
            interval_days.append(interval_date_start)
            interval_date_start += timedelta(days=1)
        interval_create_orders = self._get_intervals(len(interval_days), interval_orders)
        # for index_order in interval_create_orders:
        #     order_date = interval_days[index_order-1]
        #     qty_orders = self.test_qty_orders
        #     period_start_order = fn_time_long(order_date, order_start_time,tz_str=tz)
        #     period_end_order = fn_time_long(order_date, order_end_time, tz_str=tz)
        #     while qty_orders >0:
        #
        #         period_start_order += timedelta(minutes=20)
        #         qty_orders -=1
        while not stop_order:
            qty_day = random.randint(1, max_orders_day)
            if index_qty + qty_day > order_qty:
                qty_day = order_qty - index_qty
            index_qty += qty_day
            time_so = []
            nro = order_start_time
            for it in range(0, qty_day):
                # ndigit = random.randint(order_start_time*100, order_end_time*100)
                time_so.append(nro)
                time_int_so = random.randrange(int(order_start_time * 100), int(order_end_time * 100), 20)
                nro = round(time_int_so / 100.0, 2)

            time_so.sort()
            for iq in range(0, qty_day):
                date_time = fn_time_long(index_date, time_so[iq], tz)
                order_date_vals.append({
                    'date_order': date_time
                })
            index_date = index_date + relativedelta(days=interval_orders)
            if index_date.weekday == 6:
                index_date = (index_date + timedelta(days=1))
            if index_qty >= order_qty:
                stop_order = True
            elif index_date > order_end_date:
                index_date = order_start_date

        # _logger.info("\n\n Date orders \n\n")
        if order_date_vals:
            order_date_vals = sorted(order_date_vals, key=lambda d: d['date_order'])
        # index = 0
        # for dt in order_date_vals:
        #    _logger.info(" %s - %s  %s" % (index, dt.get('date_order').strftime('%Y-%m-%d %H:%M:%S'), dt.get('date_order')))
        #    index +=1
        return order_date_vals
        # raise ValidationError('Stop here')

    def _get_max_qty_product_random(self):
        return random.randint(1, 20)

    def _get_max_doc_lines_random(self, minimo=1, maximo=15):
        return random.randint(minimo, maximo)

    def _get_max_price_unit_random(self, minimo=10.0, maximo=500.0, rounding=2):
        return round(float_round(random.uniform(minimo, maximo), precision_digits=2), rounding)

    def _get_random_values(self, data, qty=1, model=None):
        size_data = len(data)
        vals = []
        for x in range(0, qty):
            index = random.randint(0, size_data)
            if index >= size_data:
                index -=1
            vals.append(data[index])
        return vals

    def _get_domain_customers_random(self):
        company_id = self.company_id
        cat_customer_id = self.env.ref('trn_partner_advance.pad_category_customer', raise_if_not_found=False)
        domain = [('company_id', 'in', [False,company_id.id]),
                           ('vat', 'not in', [False, '0']),
                           ('partner_code', 'not in', [False, '0', '/']),
                  ('category_id', 'in', cat_customer_id.ids)]
        if self.user_ids:
            domain += ['|', ('user_id', 'in', self.user_ids.ids), ('user_id', '=', False)]
        return domain

    def _set_invoice_line_random(self, detail):
        return [(0, 0, line) for line in detail]

    def _get_domain_products_random(self):
        company_id = self.company_id
        return [('company_id', 'in', [False,company_id.id]),
                           ('default_code', 'not in', [False, '0', '/'])] + self._get_filter_type_products()

    def _get_filter_type_products(self, only_demos=True):
        if only_demos:
            prd_tag_id = self.env.ref('trn_sale_order.prd_tag_demo_sales')
            return [('product_tag_ids', 'in', prd_tag_id.ids)]
        return []

    def _prepare_sale_order(self, **kwargs):
        # order = kwargs.get('order', False)
        # order_lines = self._prepare_order_lines(**kwargs)
        data_sale_order = {"partner_id": kwargs.get('partner_id'),
                           'partner_invoice_id': kwargs.get('partner_id'),
                           'business_name': kwargs.get('business_name'),
                           "date_order": kwargs.get('date_order', fields.Datetime.now()),
                           'user_id': kwargs.get('user_id', self.user_ids[0].id),
                           'pricelist_id': kwargs.get('pricelist_id', self.test_order_type_id.pricelist_id.id)}

                           # 'order_line': [(0, 0, line) for line in order_lines]}
        return data_sale_order

    def _prepare_order_lines(self, **kwargs):
        vals = {
            'product_uom_qty': kwargs.get('product_uom_qty', 1),
            'price_unit': kwargs.get('price_unit', random.randint(1, 10)),
            'product_id': kwargs.get('product_id', False),
            'name': kwargs.get('product_name', False),
        }
        return vals

    def _get_invoice_filtered_to_cancel(self):
        return self.invoice_ids.filtered(lambda x: x.state == 'posted' and x.state_doc not in ['A', 'N', 'C'])

    def _get_max_force_lines(self):
        return self.test_max_prd

    def _get_max_discount_per_line(self, minimo=0.01, maximo=0.12):
        return round(float_round(random.uniform(minimo, maximo), precision_digits=2), 2)

    def _get_max_additional_discount(self, minimo=0.01, maximo=0.07):
        return round(float_round((random.uniform(minimo, maximo)), precision_digits=2), 2)

    def _get_cc_number_random(self, maximum=16):
        cc_number = ""
        counter = 0
        while maximum > 0:
            if counter in [0, 1, 2, 3] or counter in [15, 16, 17, 18]:
                cc_number += str(random.randint(0, 9))
                maximum -= 1
            elif counter in [4, 9, 14]:
                cc_number += "-"
            else:
                cc_number += "0"
                maximum -= 1
        return cc_number
