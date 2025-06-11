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
    _inherit = 'sale.order.demo.wizard'

