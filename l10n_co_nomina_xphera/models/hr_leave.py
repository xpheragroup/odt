# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.model_create_multi
    def create(self, vals):
        res = super(HolidaysRequest, self).create(vals)
        print("")
        print("Entre CREATE")
        print(vals)
        print("")
        if 'holiday_status_id' in vals:
            print("")
            print(vals)
            print("")
        return res
            
    def write(self, vals):
        res = super(HolidaysRequest, self).write(vals)
        print("")
        print("Entre WRITE")
        print(vals)
        print("")
        if 'holiday_status_id' in vals:
            print("")
            print(vals['holiday_status_id'])
            print("")
        if 'request_date_from' in vals:
            print("")
            print(vals['request_date_from'])
            print("")
        if 'request_date_to' in vals:
            print("")
            print(vals['request_date_from'])
            print("")
        return res

    