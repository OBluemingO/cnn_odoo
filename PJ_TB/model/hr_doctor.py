from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError


class HrDoctor(models.Model):

    _name = "hr.doctor"
    _rec_name = "DT_name"

    DT_name = fields.Many2one(
        'res.users',
        string="Doctor name",
        domain=lambda self: [
            ("groups_id", "=", self.env.ref("PJ_TB.group_hospital_doctor").id)]
    )

    user_id = fields.Integer(
        related='DT_name.id'
    )

    related_name = fields.Char(
        related='DT_name.partner_id.name'
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

    DT_case_queue = fields.Integer(
        string='Queue For Case',
        compute='_compute_increase',
        store=True
    )

    DT_status = fields.Selection(
        [
            ("null", "ว่าง"),
            ("no null", "ไม่ว่าง"),
        ],
        string="Queue Status",
        readonly=True,
        compute='_compute_status',
        store=True
    )

    patients = fields.One2many('hr.patient', 'doctors_id')

    @api.depends('DT_case_queue')
    def _compute_status(self):
        for rec in self:
            rec.DT_status = 'null'
            if rec.DT_case_queue > 0:
                rec.DT_status = 'no null'

    @api.depends('patients.PT_status')
    def _compute_increase(self):
        for rec in self:
            list_status = rec.env['hr.patient'].search(
                [('doctors_id', '=', rec.related_name)])

            rec.DT_case_queue = 0
            if list_status:
                count = 0
                rec.DT_case_queue = 1
                for r in list_status:
                    if r.PT_status == True:
                        count += 1

                if count == len(list_status):
                    rec.DT_case_queue = 0

    @api.constrains('DT_name')
    def _check_name_doctor_unique(self):
        name_doctor = self.search_count(
            [
                ('DT_name', '=', self.DT_name.id),
                ('id', '!=', self.id)
            ]
        )
        if name_doctor > 0:
            raise ValidationError(_("Doctor already exists !"))
