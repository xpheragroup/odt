# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    pagar_festivos = fields.Boolean(string='Pagar festivos', default=False, help='Esta opción permite saber si se deben tener en cuenta las horas en días festivos.')