from odoo import api, fields, models

class PreApproveWizard(models.Model):
    _name = 'pre.approve.wizard'
    _description = 'PreApproveWizard'
    _inherit = ['multi.step.wizard.mixin']

    @api.model
    def _default_partner_id(self):
        return self.env.context.get('active_id')

    name = fields.Char(related='partner_id.name')
    partner_id = fields.Many2one(comodel_name='res.partner', name='Partner', required=True,ondelete='cascade',
                                 default=lambda self: self._default_partner_id(),
                                 )
    document_id = fields.Boolean('Document (CI)', default=False)
    photo = fields.Boolean('Photo', default=False)

    test_one = fields.Boolean('Test One', default=False)
    test_two = fields.Boolean('Test One', default=False)

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('doc', 'Documentation'),
            ('eva', 'Evaluation'),
            ('final', 'Final'),
        ]

    def state_exit_start(self):
        self.state = 'doc'

    def state_exit_doc(self):
        self.state = 'eva'

    def state_exit_eva(self):
        self.state = 'final'