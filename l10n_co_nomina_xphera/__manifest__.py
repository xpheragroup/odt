
{
    'name': 'Nómina (Xphera)',
    'version': '0.1',
    'category': 'Localization',
    'description': 'Preconfiguración Nómina (Xphera)',
    'author': 'Xphera Group S.A.S.',
    'website': 'http://xphera.co',
    'depends': [
        'hr_payroll',
        'hr_contract',
        'hr_contract_reports', 
        'hr_work_entry_holidays',
        'hr_work_entry_contract',
    ],
    'data': [
        'data/hr_payroll_co.xml',
        'views/hr_contract.xml',
        'views/hr_payslip.xml',
        'views/hr_work_entry.xml',
        'views/hr_work_entry_type.xml',
        'views/hr_rule_parameter.xml',
        'views/hr_leave_type.xml',
    ],
}