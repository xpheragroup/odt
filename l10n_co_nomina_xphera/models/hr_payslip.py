from datetime import date, datetime, timedelta
from odoo import api, fields, models, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    prima_semestre_1 = fields.Boolean(string='Pago de Primera Prima')
    prima_semestre_2 = fields.Boolean(string='Pago de Segunda Prima')
    cesantias = fields.Boolean(string='Pago de Cesantias')
    vacaciones = fields.Boolean(string='Pago de Vacaciones')

    total_extras_recargos_hours = fields.One2many('hr.payslip.total_hours', 'name', string='Total Extras y Recargos', copy=False)

    @api.onchange('contract_id')
    def set_estructure(self):
        self.struct_id = self.contract_id.tipo_contrato.id

    @api.onchange('date_from','date_to')
    def prima_cesantias(self):
        year = datetime.now().year

        primera_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DPP')],limit=1).parameter_value
        date_primera_prima = datetime.strptime(primera_prima + '/' + str(year), '%d/%m/%Y').date()
        segunda_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DSP')],limit=1).parameter_value
        date_segunda_prima = datetime.strptime(segunda_prima + '/' + str(year), '%d/%m/%Y').date()

        if (self.date_from <= date_primera_prima <= self.date_to):
            self.prima_semestre_1 = True
        elif (self.date_from <= date_segunda_prima <= self.date_to):
            self.prima_semestre_2 = True
        else:
            self.prima_semestre_1 = False
            self.prima_semestre_2 = False

        fecha_cesantias = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FCE')],limit=1).parameter_value
        date_cesantias = datetime.strptime(fecha_cesantias + '/' + str(year), '%d/%m/%Y').date()

        if (self.date_from <= date_cesantias <= self.date_to):
            self.cesantias = True
        else:
            self.cesantias = False
    
    @api.onchange('worked_days_line_ids','date_from','date_to')
    def get_hours(self):
        for line_worked_days in self.worked_days_line_ids:
            tipo_entrada = line_worked_days.work_entry_type_id
            line_worked_days.numero_horas_diurnas_ordinarias = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HDO')
            line_worked_days.numero_horas_nocturnas_ordinarias = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HNO')
            line_worked_days.numero_horas_diurnas_festivas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HDF')
            line_worked_days.numero_horas_nocturnas_festivas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HNF')
            line_worked_days.numero_horas_extras_ordinarias_diurnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HEDO')
            line_worked_days.numero_horas_extras_ordinarias_nocturnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HENO')
            line_worked_days.numero_horas_extras_festivas_diurnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HEDF')
            line_worked_days.numero_horas_extras_festivas_nocturnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HENF')

    def compute_horas(self, tipo, inicio, fin, tipo_hora):

        HDO_number = 0
        HNO_number = 0
        HDF_number = 0
        HNF_number = 0
        HEDO_number = 0
        HENO_number = 0
        HEDF_number = 0
        HENF_number = 0

        entries = self.env['hr.work.entry'].search([('work_entry_type_id','=',tipo.id),('employee_id','=',self.employee_id.id)])

        for work_entry in entries:
            work_entry_id = self.env['hr.work.entry'].search([('id','=',work_entry.id)])
            
            if work_entry_id.date_start:
                fecha_real_inicio = (work_entry_id.date_start - timedelta(hours=5)).date()
            else:
                fecha_real_inicio = datetime.today().date()

            if work_entry_id.date_stop:
                fecha_real_fin = (work_entry_id.date_stop - timedelta(hours=5)).date()
            else:
                fecha_real_fin = datetime.today().date()

            if (fecha_real_inicio >= inicio) and (fecha_real_fin <= fin):
                if tipo_hora == 'HDO':
                    HDO_number += work_entry_id.horas_diurnas_ordinarias
                if tipo_hora == 'HNO':
                    HNO_number += work_entry_id.horas_nocturnas_ordinarias
                if work_entry_id.pay_festivos:
                    if tipo_hora == 'HDF':
                        HDF_number += work_entry_id.horas_diurnas_festivas
                    if tipo_hora == 'HNF':
                        HNF_number += work_entry_id.horas_nocturnas_festivas
                if tipo_hora == 'HEDO':
                    HEDO_number += work_entry_id.horas_extras_ordinarias_diurnas
                if tipo_hora == 'HENO':
                    HENO_number += work_entry_id.horas_extras_ordinarias_nocturnas
                if work_entry_id.pay_festivos:
                    if tipo_hora == 'HEDF':
                        HEDF_number += work_entry_id.horas_extras_festivas_diurnas
                    if tipo_hora == 'HENF':
                        HENF_number += work_entry_id.horas_extras_festivas_nocturnas
                
        horas = HDO_number + HNO_number + HDF_number + HNF_number + HEDO_number + HENO_number + HEDF_number + HENF_number

        return horas
    
    @api.onchange('worked_days_line_ids')
    def get_total_hours(self):

        self.total_extras_recargos_hours = self.total_extras_recargos_hours.new()
        
        if self.name:
            self.total_extras_recargos_hours.name = str(self.id) + ' Extras y Recargos ' + self.name
        else:
            self.total_extras_recargos_hours.name = str(self.id) + ' Extras y Recargos '

        self.total_extras_recargos_hours.total_numero_horas_diurnas_ordinarias = 0
        self.total_extras_recargos_hours.total_numero_horas_nocturnas_ordinarias = 0
        self.total_extras_recargos_hours.total_numero_horas_diurnas_festivas = 0
        self.total_extras_recargos_hours.total_numero_horas_nocturnas_festivas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_ordinarias_diurnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_ordinarias_nocturnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_festivas_diurnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_festivas_nocturnas = 0

        for line_worked_days in self.worked_days_line_ids:
            for line_total_houres in self.total_extras_recargos_hours:
                line_total_houres.total_numero_horas_diurnas_ordinarias += line_worked_days.numero_horas_diurnas_ordinarias
                line_total_houres.total_numero_horas_nocturnas_ordinarias += line_worked_days.numero_horas_nocturnas_ordinarias
                line_total_houres.total_numero_horas_diurnas_festivas += line_worked_days.numero_horas_diurnas_festivas
                line_total_houres.total_numero_horas_nocturnas_festivas += line_worked_days.numero_horas_nocturnas_festivas
                line_total_houres.total_numero_horas_extras_ordinarias_diurnas += line_worked_days.numero_horas_extras_ordinarias_diurnas
                line_total_houres.total_numero_horas_extras_ordinarias_nocturnas += line_worked_days.numero_horas_extras_ordinarias_nocturnas
                line_total_houres.total_numero_horas_extras_festivas_diurnas += line_worked_days.numero_horas_extras_festivas_diurnas
                line_total_houres.total_numero_horas_extras_festivas_nocturnas += line_worked_days.numero_horas_extras_festivas_nocturnas

    def compute_sheet(self):     
        res = super(HrPayslip, self).compute_sheet()

        mes = self.date_from.month

        percentage_prima = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','PS')],limit=1).parameter_value)
        percentage_cesantias = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','CES')],limit=1).parameter_value)
        percentage_intereses_cesantias = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','ICE')],limit=1).parameter_value)
        percentage_vacaciones = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','PVAC')],limit=1).parameter_value)

        
        if mes == 1:
            self.contract_id.prima_1 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_1 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_1 = self.contract_id.cesantias_1 * percentage_intereses_cesantias
            self.contract_id.vacaciones_1 = self.get_devengado() * percentage_vacaciones
        if mes == 2:
            self.contract_id.prima_2 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_2 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_2 = self.contract_id.cesantias_2 * percentage_intereses_cesantias
            self.contract_id.vacaciones_2 = self.get_devengado() * percentage_vacaciones
        if mes == 3:
            self.contract_id.prima_3 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_3 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_3 = self.contract_id.cesantias_3 * percentage_intereses_cesantias
            self.contract_id.vacaciones_3 = self.get_devengado() * percentage_vacaciones
        if mes == 4:
            self.contract_id.prima_4 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_4 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_4 = self.contract_id.cesantias_4 * percentage_intereses_cesantias
            self.contract_id.vacaciones_4 = self.get_devengado() * percentage_vacaciones
        if mes == 5:
            self.contract_id.prima_5 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_5 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_5 = self.contract_id.cesantias_5 * percentage_intereses_cesantias
            self.contract_id.vacaciones_5 = self.get_devengado() * percentage_vacaciones
        if mes == 6:
            self.contract_id.prima_6 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_6 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_6 = self.contract_id.cesantias_6 * percentage_intereses_cesantias
            self.contract_id.vacaciones_6 = self.get_devengado() * percentage_vacaciones
        if mes == 7:
            self.contract_id.prima_7 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_7 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_7 = self.contract_id.cesantias_7 * percentage_intereses_cesantias
            self.contract_id.vacaciones_7 = self.get_devengado() * percentage_vacaciones
        if mes == 8:
            self.contract_id.prima_8 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_8 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_8 = self.contract_id.cesantias_8 * percentage_intereses_cesantias
            self.contract_id.vacaciones_8 = self.get_devengado() * percentage_vacaciones
        if mes == 9:
            self.contract_id.prima_9 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_9 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_9 = self.contract_id.cesantias_9 * percentage_intereses_cesantias
            self.contract_id.vacaciones_9 = self.get_devengado() * percentage_vacaciones
        if mes == 10:
            self.contract_id.prima_10 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_10 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_10 = self.contract_id.cesantias_10 * percentage_intereses_cesantias
            self.contract_id.vacaciones_10 = self.get_devengado() * percentage_vacaciones
        if mes == 11:
            self.contract_id.prima_11 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_11 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_11 = self.contract_id.cesantias_11 * percentage_intereses_cesantias
            self.contract_id.vacaciones_11 = self.get_devengado() * percentage_vacaciones
        if mes == 12:
            self.contract_id.prima_12 = self.get_devengado() * (percentage_prima/6)
            self.contract_id.cesantias_12 = self.contract_id.wage * (percentage_cesantias/6)
            self.contract_id.intereses_cesantias_12 = self.contract_id.cesantias_12 * percentage_intereses_cesantias
            self.contract_id.vacaciones_12 = self.get_devengado() * percentage_vacaciones

        return res
    
    def get_devengado(self):
        for line in self.line_ids:
            if line.code == 'DEV':
                return line.total
    
class TotalHoursPayslip(models.Model):
    _name = 'hr.payslip.total_hours'

    name = fields.Char()
    total_numero_horas_diurnas_ordinarias = fields.Float(string='Total Horas Diurnas Ordinales')
    total_numero_horas_nocturnas_ordinarias = fields.Float(string='Total Horas Nocuturna Ordinales')
    total_numero_horas_diurnas_festivas = fields.Float(string='Total Horas Diurnas Festivas')
    total_numero_horas_nocturnas_festivas = fields.Float(string='Total Horas Nocuturna Festivas')
    total_numero_horas_extras_ordinarias_diurnas = fields.Float(string='Total Horas Extra Ordinarias Diurnas')
    total_numero_horas_extras_ordinarias_nocturnas = fields.Float(string='Total Horas Extra Ordinarias Nocturnas')
    total_numero_horas_extras_festivas_diurnas = fields.Float(string='Total Horas Extra Diurnas Festivas')
    total_numero_horas_extras_festivas_nocturnas = fields.Float(string='Total Horas Extra Nocturnas Festivas')