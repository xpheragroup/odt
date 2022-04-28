from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'

    def _one_wage_type(self, context=None):
        return [('monthly', 'Salario Fijo Mensual')]

    def _one_default_schedule_pay(self, context=None):
        return [('monthly', 'Mensual')]

    wage_type = fields.Selection(_one_wage_type, default='monthly', required=True)
    default_schedule_pay = fields.Selection(_one_default_schedule_pay, default='monthly', required=True)