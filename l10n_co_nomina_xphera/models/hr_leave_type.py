
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    limite = fields.Boolean(string='Límite de Tiempo')
    cantidad_limite = fields.Float(string='Tiempo Límite')
    notas = fields.Char(string='Notas')

    def _add_semana(self, context=None):
        return [('day', 'Día'), ('half_day', 'Medio día'), ('hour', 'Horas'), ('semana','Semana')]

    request_unit = fields.Selection(_add_semana)