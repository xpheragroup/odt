# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from odoo import api, fields, models

class HrSalaryRuleParameter(models.Model):
    _inherit = 'hr.rule.parameter'

    es_festivo = fields.Boolean(string='Festivo', default=False, help='Si el parametro corresponde a una fecha festiva debe ser marcada esta casilla ')