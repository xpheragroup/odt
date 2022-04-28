from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    auxilio_transporte = fields.Boolean(string='Auxilio de Transporte', help='La empresa da a sus empleados auxilio de transporte. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    auxilio_conectividad = fields.Boolean(string='Auxilio de Conectividad', help='La empresa da a sus empleados auxilio de conectividad. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    
    prima_1 = fields.Float(string='Primas Enero')
    prima_2 = fields.Float(string='Primas Febrero')
    prima_3 = fields.Float(string='Primas Marzo')
    prima_4 = fields.Float(string='Primas Abril')
    prima_5 = fields.Float(string='Primas Mayo')
    prima_6 = fields.Float(string='Primas Junio')
    prima_7 = fields.Float(string='Primas Julio')
    prima_8 = fields.Float(string='Primas Agosto')
    prima_9 = fields.Float(string='Primas Septiembre')
    prima_10 = fields.Float(string='Primas Octubre')
    prima_11 = fields.Float(string='Primas Noviembre')
    prima_12 = fields.Float(string='Primas Diciembre')

    total_prima_1 = fields.Float(string='Primas Semestre 1', compute='_compute_total_prima_1')
    total_prima_2 = fields.Float(string='Primas Semestre 2', compute='_compute_total_prima_2')

    @api.depends('prima_1','prima_2','prima_3','prima_4','prima_5','prima_6')
    def _compute_total_prima_1(self):
        self.total_prima_1 = self.prima_1 + self.prima_2 + self.prima_3 + self.prima_4 + self.prima_5 + self.prima_6
    
    @api.depends('prima_7','prima_8','prima_9','prima_10','prima_11','prima_12')
    def _compute_total_prima_2(self):
        self.total_prima_2 = self.prima_7 + self.prima_8 + self.prima_9 + self.prima_10 + self.prima_11 + self.prima_12

    cesantias_1 = fields.Float(string='Cesantias Enero')
    cesantias_2 = fields.Float(string='Cesantias Febrero')
    cesantias_3 = fields.Float(string='Cesantias Marzo')
    cesantias_4 = fields.Float(string='Cesantias Abril')
    cesantias_5 = fields.Float(string='Cesantias Mayo')
    cesantias_6 = fields.Float(string='Cesantias Junio')
    cesantias_7 = fields.Float(string='Cesantias Julio')
    cesantias_8 = fields.Float(string='Cesantias Agosto')
    cesantias_9 = fields.Float(string='Cesantias Septiembre')
    cesantias_10 = fields.Float(string='Cesantias Octubre')
    cesantias_11 = fields.Float(string='Cesantias Noviembre')
    cesantias_12 = fields.Float(string='Cesantias Diciembre')

    intereses_cesantias_1 = fields.Float(string='Int Cesantia Enero')
    intereses_cesantias_2 = fields.Float(string='Int Cesantia Febrero')
    intereses_cesantias_3 = fields.Float(string='Int Cesantia Marzo')
    intereses_cesantias_4 = fields.Float(string='Int Cesantia Abril')
    intereses_cesantias_5 = fields.Float(string='Int Cesantia Mayo')
    intereses_cesantias_6 = fields.Float(string='Int Cesantia Junio')
    intereses_cesantias_7 = fields.Float(string='Int Cesantia Julio')
    intereses_cesantias_8 = fields.Float(string='Int Cesantia Agosto')
    intereses_cesantias_9 = fields.Float(string='Int Cesantia Septiembre')
    intereses_cesantias_10 = fields.Float(string='Int Cesantia Octubre')
    intereses_cesantias_11 = fields.Float(string='Int Cesantia Noviembre')
    intereses_cesantias_12 = fields.Float(string='Int Cesantia Diciembre')

    total_cesantias_year = fields.Float(string='Total Cesantias del Año', compute='_compute_total_cesantias_year')
    total_intereses_cesantias_year = fields.Float(string='Total Intereses Cesantias del Año', compute='_compute_total_intereses_cesantias_year')

    @api.depends('cesantias_1','cesantias_2','cesantias_3','cesantias_4','cesantias_5','cesantias_6','cesantias_7','cesantias_8','cesantias_9','cesantias_10','cesantias_11','cesantias_12')
    def _compute_total_cesantias_year(self):
        self.total_cesantias_year = self.cesantias_1 + self.cesantias_2 + self.cesantias_3 + self.cesantias_4 + self.cesantias_5 + self.cesantias_6 + self.cesantias_7 + self.cesantias_8 + self.cesantias_9 + self.cesantias_10 + self.cesantias_11 + self.cesantias_12

    @api.depends('intereses_cesantias_1','intereses_cesantias_2','intereses_cesantias_3','intereses_cesantias_4','intereses_cesantias_5','intereses_cesantias_6','intereses_cesantias_7','intereses_cesantias_8','intereses_cesantias_9','intereses_cesantias_10','intereses_cesantias_11','intereses_cesantias_12')
    def _compute_total_intereses_cesantias_year(self):
        self.total_intereses_cesantias_year = self.intereses_cesantias_1 + self.intereses_cesantias_2 + self.intereses_cesantias_3 + self.intereses_cesantias_4 + self.intereses_cesantias_5 + self.intereses_cesantias_6 + self.intereses_cesantias_7 + self.intereses_cesantias_8 + self.intereses_cesantias_9 + self.intereses_cesantias_10 + self.intereses_cesantias_11 + self.intereses_cesantias_12

    vacaciones_1 = fields.Float(string='Vacacion Enero')
    vacaciones_2 = fields.Float(string='Vacacion Febrero')
    vacaciones_3 = fields.Float(string='Vacacion Marzo')
    vacaciones_4 = fields.Float(string='Vacacion Abril')
    vacaciones_5 = fields.Float(string='Vacacion Mayo')
    vacaciones_6 = fields.Float(string='Vacacion Junio')
    vacaciones_7 = fields.Float(string='Vacacion Julio')
    vacaciones_8 = fields.Float(string='Vacacion Agosto')
    vacaciones_9 = fields.Float(string='Vacacion Septiembre')
    vacaciones_10 = fields.Float(string='Vacacion Octubre')
    vacaciones_11 = fields.Float(string='Vacacion Noviembre')
    vacaciones_12 = fields.Float(string='Vacacion Diciembre')

    total_vacaciones = fields.Float(string='Total Vacaciones', compute='_compute_total_vacaciones')

    riesgo = fields.Selection([
        ('1', 'Riesgo I'),
        ('2', 'Riesgo II'),
        ('3', 'Riesgo III'),
        ('4', 'Riesgo IV'),
        ('5', 'Riesgo V')], string='Riesgo ARL')

    salary_type = fields.Selection([
        ('1', 'Ordinario'),
        ('2', 'Integral'),
        ('3', 'En especie')], string='Tipo de Salario')

    tipo_contrato = fields.Many2one('hr.payroll.structure', string='Tipo de Contrato')

    libranzas_CCF = fields.Monetary(string='Libranzas con CCF', help='En el caso de que el empleado deba pagar una libranza, se debe establecer el monto que se descontará de la nómina mensualmente.')
    libranzas_coperatica = fields.Monetary(string='Libranzas con Coperativas', help='En el caso de que el empleado deba pagar credito con una coperativa, se debe establecer el monto que se descontará de la nómina mensualmente.')
    credito_banco = fields.Monetary(string='Credito Bancario', help='En el caso de que el empleado deba pagar un credito bancario, se debe establecer el monto que se descontará de la nómina mensualmente.')

    embargo_judicial = fields.Monetary(string='Embargo Judicial', help='Descuentos aplicados por nomina al trabajador para cancelar sobre actuaciones judiciales debidamente motivadas.')

    aux_educacion = fields.Monetary(string='Auxilio Educación')
    aux_vivienda = fields.Monetary(string='Auxilio Vivienda')
    aportes_AFP = fields.Monetary(string='Aportes Voluntarios a AFP')
    aux_alimentacion = fields.Monetary(string='Auxilio Alimentación')
    bonificacion = fields.Monetary(string='Bonificaciones')

    @api.depends('vacaciones_1','vacaciones_2','vacaciones_3','vacaciones_4','vacaciones_5','vacaciones_6','vacaciones_7','vacaciones_8','vacaciones_9','vacaciones_10','vacaciones_11','vacaciones_12')
    def _compute_total_vacaciones(self):
        self.total_vacaciones = self.vacaciones_1 + self.vacaciones_2 + self.vacaciones_3 + self.vacaciones_4 + self.vacaciones_5 + self.vacaciones_6 + self.vacaciones_7 + self.vacaciones_8 + self.vacaciones_9 + self.vacaciones_10 + self.vacaciones_11 + self.vacaciones_12

    @api.onchange('auxilio_transporte')
    def just_auxilio_transporte(self):
        if self.auxilio_transporte:
            self.auxilio_conectividad = False

    @api.onchange('auxilio_conectividad')
    def just_auxilio_conectividad(self):
        if self.auxilio_conectividad:
            self.auxilio_transporte = False

    @api.model
    def create(self, vals):
        contracts = super(HrContract, self).create(vals)
        SMMLV = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','SMMLV')],limit=1).parameter_value)
        
        if ('tipo_contrato' in vals):
            name_contract = self.env['hr.payroll.structure'].search([('id','=',vals.get('tipo_contrato'))],limit=1).name

        if ('wage' in vals) and ('tipo_contrato' in vals):
            if (vals.get('wage') < SMMLV) and (name_contract != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))
        elif ('wage' in vals):
            if (vals.get('wage') < SMMLV) and (self.tipo_contrato.name != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))
        elif ('tipo_contrato' in vals):
            if (self.wage < SMMLV) and (name_contract != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))

        return contracts

    def write(self, vals):
        res = super(HrContract, self).write(vals)
        SMMLV = float(self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','SMMLV')],limit=1).parameter_value)
        
        if 'tipo_contrato' in vals:
            name_contract = self.env['hr.payroll.structure'].search([('id','=',vals.get('tipo_contrato'))],limit=1).name

        if ('wage' in vals) and ('tipo_contrato' in vals):
            if (vals.get('wage') < SMMLV) and (name_contract != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))
        elif 'wage' in vals:
            if (vals.get('wage') < SMMLV) and (self.tipo_contrato.name != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))
        elif 'tipo_contrato' in vals:
            if (self.wage < SMMLV) and (name_contract != 'Contrato de Aprendizaje'):
                raise UserError(_("El salario no puede ser menor a " + str(SMMLV) + "."))

        return res