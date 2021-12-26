from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError


class HrDoctor(models.Model):

    _name = "hr.doctor"
    _rec_name = "DT_name"

    DT_name = fields.Char(
        string="Name"
    )

    DT_age = fields.Integer(
        string="Age"
    )

    DT_gender = fields.Selection(
        [
            ("ชาย", "ชาย"),
            ("หญิง", "หญิง"),
            ("อื่นๆ", "อื่นๆ"),
        ],
        string="Gender",
        default="ชาย",
        required=True
    )

    patient_totals = fields.One2many(
        'hr.patient',
        'doctors_id',
    )
