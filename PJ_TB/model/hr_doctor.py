from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError


class HrDoctor(models.Model):

    _name = "hr.doctor"
    _rec_name = "DT_name"

    DT_name = fields.Many2one(
        'res.users',
        string="Doctor name",
        domain=lambda self: [
            ("groups_id", "=", self.env.ref("PJ_TB.group_hospital_doctor").id)]
    )

    related_name = fields.Char(
        related='DT_name.partner_id.name'
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

    DT_case_queue = fields.Integer(
        string='Queue For Case',
        compute='_compute_increase'
    )

    DT_status = fields.Selection(
        [
            ("null", "ว่าง"),
            ("no null", "ไม่ว่าง"),
        ],
        string="Queue Status",
        readonly=True,
        compute='_compute_status',
        default='null'
    )

    patients = fields.One2many('hr.patient', 'doctors_id')

    @api.depends('DT_case_queue')
    def _compute_status(self):
        for rec in self:
            print(rec.DT_case_queue, 'rec.DT_case_queue')
            rec.DT_status = 'null'
            if rec.DT_case_queue > 0:
                print('1111111111111111111111111111')
                rec.DT_status = 'no null'

    def _compute_increase(self):
        list_status = self.env['hr.patient'].search(
            [('doctors_id', '=', self.related_name)])
        for rec in self:
            rec.DT_case_queue = 0
            if list_status:
                count = 0
                rec.DT_case_queue = 1
                for r in list_status:
                    if r.PT_status == True:
                        count += 1

                if count == len(list_status):
                    rec.DT_case_queue = 0
