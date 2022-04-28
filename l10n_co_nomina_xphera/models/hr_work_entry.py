# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    pay_festivos = fields.Boolean(string='Pagar festivos', default=False, help='Esta opción permite saber si se deben tener en cuenta las horas en días festivos.')

    @api.onchange('work_entry_type_id')
    def _pagar_festivos(self):
        if self.work_entry_type_id.pagar_festivos:
            self.pay_festivos = True
        else:
            self.pay_festivos = False

    @api.depends('date_start','date_stop','employee_id')
    def _calculo_horas(self):

        year = datetime.now().year
        fecha = date(year,1,1)
        fecha += timedelta(days=6-fecha.weekday())
        domingos=[]
        while fecha.year == year:
            domingos.append(fecha)
            fecha += timedelta(days=7)
        
        if self.date_start:
            fecha_real_inicio = (self.date_start - timedelta(hours=5))
        else:
            fecha_real_inicio = datetime.today()

        if self.date_stop:
            fecha_real_fin = (self.date_stop - timedelta(hours=5))
        else:
            fecha_real_fin = datetime.today()

        morning = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','HM')],limit=1).parameter_value
        hour_morning = datetime.strptime(morning, '%H:%M').time().hour
        afternoon = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','HT')],limit=1).parameter_value
        hour_afternoon = datetime.strptime(afternoon, '%H:%M').time().hour

        festivos = []
        days_festivos = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.es_festivo','=',True)])

        for day_fest in days_festivos:
            dia = datetime.strptime(day_fest.parameter_value + '/' + str(year), '%d/%m/%Y').date()
            festivos.append(dia)

        domingos_festivos = festivos + domingos

        self.horas_diurnas_ordinarias = 0
        self.horas_nocturnas_ordinarias = 0
        self.horas_diurnas_festivas = 0
        self.horas_nocturnas_festivas = 0
        
        self.horas_extras_ordinarias_diurnas = 0
        self.horas_extras_ordinarias_nocturnas = 0
        self.horas_extras_festivas_diurnas = 0
        self.horas_extras_festivas_nocturnas = 0

        fecha_conteo = fecha_real_inicio
        day_conteo = fecha_real_inicio.day
        mes_conteo = fecha_real_inicio.month

        hr_cero = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+'00', '%d/%m/%Y %H')
        hr_morning = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+str(hour_morning), '%d/%m/%Y %H')
        hr_afternoon = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+str(hour_afternoon), '%d/%m/%Y %H')
        hr_final = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+'23'+':'+'59'+':'+'59', '%d/%m/%Y %H:%M:%S')

        while fecha_conteo < fecha_real_fin:
            if fecha_conteo == fecha_real_inicio:
                if hr_morning < fecha_real_fin:
                    if hr_cero <= fecha_conteo < hr_morning:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_morning - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                        else:
                            self.horas_nocturnas_ordinarias += (hr_morning - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                else:
                    if hr_cero <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_afternoon < fecha_real_fin:
                    if hr_morning <= fecha_conteo < hr_afternoon:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (hr_afternoon - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                        else:
                            self.horas_diurnas_ordinarias += (hr_afternoon - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                else:
                    if hr_morning <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_diurnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_final < fecha_real_fin:
                    if hr_afternoon <= fecha_conteo <= hr_final:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_final - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                        else:
                            self.horas_nocturnas_ordinarias += (hr_final - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                else:
                    if hr_afternoon <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

            else:
                if hr_morning < fecha_real_fin:
                    if hr_cero <= fecha_conteo < hr_morning:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_morning - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                        else:
                            self.horas_nocturnas_ordinarias += (hr_morning - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                else:
                    if hr_cero <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_afternoon < fecha_real_fin:
                    if hr_morning <= fecha_conteo < hr_afternoon:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (hr_afternoon - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                        else:
                            self.horas_diurnas_ordinarias += (hr_afternoon - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                else:
                    if hr_morning <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (fecha_real_fin - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_diurnas_ordinarias += (fecha_real_fin - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_final < fecha_real_fin:
                    if hr_afternoon <= fecha_conteo <= hr_final:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_final - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                        else:
                            self.horas_nocturnas_ordinarias += (hr_final - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                else:
                    if hr_afternoon <= fecha_conteo <= fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

            hr_morning += timedelta(days=1)
            hr_afternoon += timedelta(days=1)
            hr_final += timedelta(days=1)
        
        self.horas_diurnas_ordinarias = round(self.horas_diurnas_ordinarias)
        self.horas_nocturnas_ordinarias = round(self.horas_nocturnas_ordinarias)
        self.horas_diurnas_festivas = round(self.horas_diurnas_festivas)
        self.horas_nocturnas_festivas = round(self.horas_nocturnas_festivas)
        
        self.horas_extras_ordinarias_diurnas = round(self.horas_extras_ordinarias_diurnas)
        self.horas_extras_ordinarias_nocturnas = round(self.horas_extras_ordinarias_nocturnas)
        self.horas_extras_festivas_diurnas = round(self.horas_extras_festivas_diurnas)
        self.horas_extras_festivas_nocturnas = round(self.horas_extras_festivas_nocturnas)
        
    horas_diurnas_ordinarias = fields.Float(string='Horas Diurnas Ordinales', compute=_calculo_horas)
    horas_nocturnas_ordinarias = fields.Float(string='Horas Nocuturna Ordinales', compute=_calculo_horas)
    horas_diurnas_festivas = fields.Float(string='Horas Diurnas Festivas', compute=_calculo_horas)
    horas_nocturnas_festivas = fields.Float(string='Horas Nocuturna Festivas', compute=_calculo_horas)
    
    horas_extras_ordinarias_diurnas = fields.Float(string='Horas Extra Ordinarias Diurnas', compute=_calculo_horas)
    horas_extras_ordinarias_nocturnas = fields.Float(string='Horas Extra Ordinarias Nocturnas', compute=_calculo_horas)
    horas_extras_festivas_diurnas = fields.Float(string='Horas Extra Diurnas Festivas', compute=_calculo_horas)
    horas_extras_festivas_nocturnas = fields.Float(string='Horas Extra Nocturnas Festivas', compute=_calculo_horas)
    
    def dupla_horas(self, fecha_inicio, fecha_fin):
        dupla = [(fecha_inicio.hour + (fecha_inicio.minute/60.0) + (fecha_inicio.minute/(60.0*60.0))),(fecha_fin.hour + (fecha_fin.minute/60.0) + (fecha_fin.minute/(60.0*60.0)))]
        return dupla

    def compute_horas_extra(self, dupla, day):
        intersecto = []
        horas = 0
        rango = []
        
        horas_lunes_empleado = 0
        horas_martes_empleado = 0
        horas_miercoles_empleado = 0
        horas_jueves_empleado = 0
        horas_viernes_empleado = 0
        horas_sabado_empleado = 0
        horas_domingo_empleado = 0

        rangos_horas_lunes = []
        rangos_horas_martes = []
        rangos_horas_miercoles = []
        rangos_horas_jueves = []
        rangos_horas_viernes = []
        rangos_horas_sabado = []
        rangos_horas_domingo = []

        for horario in self.employee_id.resource_calendar_id.attendance_ids:
            horas_empleado = horario.hour_to - horario.hour_from
            rangos = [horario.hour_from,horario.hour_to]

            if horario.dayofweek == '0':
                horas_lunes_empleado += horas_empleado
                rangos_horas_lunes.append(rangos)
            if horario.dayofweek == '1':
                horas_martes_empleado += horas_empleado
                rangos_horas_martes.append(rangos)
            if horario.dayofweek == '2':
                horas_miercoles_empleado += horas_empleado
                rangos_horas_miercoles.append(rangos)
            if horario.dayofweek == '3':
                horas_jueves_empleado += horas_empleado
                rangos_horas_jueves.append(rangos)
            if horario.dayofweek == '4':
                horas_viernes_empleado += horas_empleado
                rangos_horas_viernes.append(rangos)
            if horario.dayofweek == '5':
                horas_sabado_empleado += horas_empleado
                rangos_horas_sabado.append(rangos)
            if horario.dayofweek == '6':
                horas_domingo_empleado += horas_empleado
                rangos_horas_domingo.append(rangos)

        if day == 'Monday':
            rango = rangos_horas_lunes
        if day == 'Tuesday':
            rango = rangos_horas_martes
        if day == 'Wednesday':
            rango = rangos_horas_miercoles
        if day == 'Thursday':
            rango = rangos_horas_jueves
        if day == 'Friday':
            rango = rangos_horas_viernes
        if day == 'Saturday':
            rango = rangos_horas_sabado
        if day == 'Sunday':
            rango = rangos_horas_domingo

        for i in rango:
            i1 = dupla[0]
            f1 = dupla[1]
            i2 = i[0]
            f2 = i[1]
            if ((f1>=i2 and f1<=f2) or (f2>=i1 and f2<=f1)):
                start=0
                end=0
                start = i1 if i1>i2 else i2
                end = f1 if f1<f2 else f2
                intersecto.append([start,end])
        
        horas_dupla = dupla[1] - dupla[0]
        horas_intersecto = 0
        for inter in intersecto:
            horas_intersecto += inter[1] - inter[0]
        
        if horas_dupla - horas_intersecto > 0:
            horas = horas_dupla - horas_intersecto

        return horas
    
    @api.model_create_multi
    def create(self, vals_list):
        work_entries = super(HrWorkEntry, self).create(vals_list)
        
        max_horas_extra_day = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','MHED')],limit=1).parameter_value)
        max_horas_extra_semana = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','MHES')],limit=1).parameter_value)

        if len(work_entries) == 1:
            if work_entries.date_start:
                fecha_real_inicio = (work_entries.date_start - timedelta(hours=5))
            else:
                fecha_real_inicio = datetime.today()
            
            entradas = self.env['hr.work.entry'].search([('employee_id','=',work_entries.employee_id.id)])

            fecha = fecha_real_inicio.date().toordinal()
            ultimo_domingo = fecha - (fecha % 7)
            proximo_domingo = ultimo_domingo + 7

            horas_extra_entradas_today = 0
            horas_extra_entradas_semana = 0

            for horas_entradas in entradas:
                day_start = (horas_entradas.date_start - timedelta(hours=5)).date()
                entradas_id = self.env['hr.work.entry'].search([('id','=',horas_entradas.id)])

                if day_start == fecha_real_inicio.date():
                    horas_extra_entradas_today += entradas_id.horas_extras_ordinarias_diurnas + entradas_id.horas_extras_ordinarias_nocturnas + entradas_id.horas_extras_festivas_diurnas + entradas_id.horas_extras_festivas_nocturnas 

                if date.fromordinal(ultimo_domingo) < day_start <= date.fromordinal(proximo_domingo):
                    horas_extra_entradas_semana += entradas_id.horas_extras_ordinarias_diurnas + entradas_id.horas_extras_ordinarias_nocturnas + entradas_id.horas_extras_festivas_diurnas + entradas_id.horas_extras_festivas_nocturnas
            
            if horas_extra_entradas_today > max_horas_extra_day:
                raise UserError(_("La cantidad de horas extra por día es mayor a las " + str(max_horas_extra_day) + " horas permitidas."))
            
            if horas_extra_entradas_semana > max_horas_extra_semana:
                raise UserError(_("La cantidad de horas extra en la semana actual es mayor a las " + str(max_horas_extra_semana) + " horas permitidas."))
        
        return work_entries
    

    def write(self, vals):
        work_entries = super(HrWorkEntry, self).write(vals)
        
        max_horas_extra_day = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','MHED')],limit=1).parameter_value)
        max_horas_extra_semana = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','MHES')],limit=1).parameter_value)

        if ('date_start' in vals) or ('date_stop' in vals):
            if 'date_start' in vals:
                fecha_real_inicio = (datetime.strptime(vals['date_start'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=5))
            else:
                fecha_real_inicio = (self.date_start - timedelta(hours=5))
            
            if 'employee_id' in vals:
                entradas = self.env['hr.work.entry'].search([('employee_id','=',vals['employee_id'])])
            else:
                entradas = self.env['hr.work.entry'].search([('employee_id','=',self.employee_id.id)])

            fecha = fecha_real_inicio.date().toordinal()
            ultimo_domingo = fecha - (fecha % 7)
            proximo_domingo = ultimo_domingo + 7

            horas_extra_entradas_today = 0
            horas_extra_entradas_semana = 0

            for horas_entradas in entradas:
                day_start = (horas_entradas.date_start - timedelta(hours=5)).date()
                entradas_id = self.env['hr.work.entry'].search([('id','=',horas_entradas.id)])

                if day_start == fecha_real_inicio.date():
                    horas_extra_entradas_today += entradas_id.horas_extras_ordinarias_diurnas + entradas_id.horas_extras_ordinarias_nocturnas + entradas_id.horas_extras_festivas_diurnas + entradas_id.horas_extras_festivas_nocturnas 

                if date.fromordinal(ultimo_domingo) < day_start <= date.fromordinal(proximo_domingo):
                    horas_extra_entradas_semana += entradas_id.horas_extras_ordinarias_diurnas + entradas_id.horas_extras_ordinarias_nocturnas + entradas_id.horas_extras_festivas_diurnas + entradas_id.horas_extras_festivas_nocturnas
            
            if horas_extra_entradas_today > max_horas_extra_day:
                raise UserError(_("La cantidad de horas extra por día es mayor a las " + str(max_horas_extra_day) + " horas permitidas."))
            
            if horas_extra_entradas_semana > max_horas_extra_semana:
                raise UserError(_("La cantidad de horas extra en la semana actual es mayor a las " + str(max_horas_extra_semana) + " horas permitidas."))
        
        return work_entries