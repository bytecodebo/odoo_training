import random
from datetime import timedelta

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
