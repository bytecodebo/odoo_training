# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PartnerStage(models.Model):
    _inherit = "res.partner.stage"

    state = fields.Selection(
        selection_add=[("pre_select", "Pre Approved"), ("confirmed",)],
        ondelete={'pre_select': 'cascade'}
    )
