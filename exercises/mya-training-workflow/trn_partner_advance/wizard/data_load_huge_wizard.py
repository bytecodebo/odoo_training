from xml.dom import ValidationErr

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class DataLoadHugeWizard(models.TransientModel):
    _name = 'data.load.huge.wizard'
    _description = 'Load huge data'

    load_type = fields.Selection([('partner', 'Partners')])
    # test_mode = fields.Boolean(default=False)
    quantities = fields.Integer(default=10)

    def action_process(self):
        test_mode = self._context.get('ctx_test_mode',False)
        if not self.load_type:
            raise ValidationError(_(" Select a load type"))
        if self.load_type == 'partner':
            ctx = {'ctx_partner_qty_demo': self.quantities}
            values = {'description': 'Carga Masiva de Clientes',
                      'priority': 8,
                      'eta': fields.Datetime.now() + timedelta(seconds=30)}
            print('vals', values)
            self.env['res.partner'].with_context(**ctx).with_delay(**values).action_create_partner_demos()
        return True


