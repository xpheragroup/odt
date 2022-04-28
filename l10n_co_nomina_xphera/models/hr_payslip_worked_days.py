from datetime import date, datetime, timedelta
from odoo import api, fields, models

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    numero_horas_diurnas_ordinarias = fields.Float(string='Horas Diurnas Ordinales')
    numero_horas_nocturnas_ordinarias = fields.Float(string='Horas Nocuturna Ordinales')
    numero_horas_diurnas_festivas = fields.Float(string='Horas Diurnas Festivas')
    numero_horas_nocturnas_festivas = fields.Float(string='Horas Nocuturna Festivas')
    numero_horas_extras_ordinarias_diurnas = fields.Float(string='Horas Extra Ordinarias Diurnas')
    numero_horas_extras_ordinarias_nocturnas = fields.Float(string='Horas Extra Ordinarias Nocturnas')
    numero_horas_extras_festivas_diurnas = fields.Float(string='Horas Extra Diurnas Festivas')
    numero_horas_extras_festivas_nocturnas = fields.Float(string='Horas Extra Nocturnas Festivas')