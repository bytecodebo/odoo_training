from xml.dom import ValidationErr

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class DataLoadHugeWizard(models.TransientModel):
    _name = 'data.load.huge.wizard'
    _description = 'Load huge data'

    load_type = fields.Selection([('partner', 'Partners')])
    # test_mode = fields.Boolean(default=False)
    quantities = fields.Integer(default=5000)
    interval = fields.Integer(default=100)

    def action_process(self):
        test_mode = self._context.get('ctx_test_mode',False)
        if not self.load_type:
            raise ValidationError(_(" Select a load type"))
        if self.load_type == 'partner':
            qty  = self.quantities
            interval = self.interval
            start = fields.Datetime.now()
            interval_seconds = 30
            registered = 0
            while qty >0:
                ctx = {'ctx_partner_qty_demo': interval}
                values = {'description': 'Carga Masiva de Clientes',
                          'priority': 8,
                          'eta': start + timedelta(seconds=interval_seconds)}
                self.env['res.partner'].with_context(**ctx).with_delay(**values).action_create_partner_demos()
                interval_seconds += 30
                qty -= interval
                registered += interval
                print("\n\n **** customer registered %s of %s \n\n" % (registered, self.quantities))
        return True

