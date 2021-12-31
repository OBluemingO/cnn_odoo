from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import pytz


class Lab(models.Model):
    _name = "ir.lab"
    _rec_name = "lab_seq"

    lab_seq = fields.Char(
        string="Lab Number", readonly=True, required=True, copy=False, default="New"
    )

    lab_type = fields.Selection(
        selection=[
            ("blood test", "Blood Test"),
            ("tb test", "Tubercusius Image Predict"),
        ],
        string="Test Type",
        default="blood test",
        required=True,
    )

    lab_doctor = fields.Char(
        string="Doctor", default=lambda self: self.create_by_doctor()
    )

    lab_date = fields.Char(
        string="Date of Analysis",
        compute='cumpute_auto_date',
        store=True,
    )

    lab_date_end = fields.Char(
        string="Date of Complate",
        compute='cumpute_auto_date_end',
        store=True,
    )

    lab_state = fields.Selection(
        selection=[
            ("draft", "DRRAFT"),
            ("test", "TEST IN PROGRESS"),
            ("complate", "COMPLETED"),
            ("invoice", "INVOICED"),
        ],
        default="draft",
        string="State",
    )

    patient_id = fields.Many2one(
        "hr.patient",
        required=True,
    )

    lab_tests = fields.One2many(
        'ir.lab_test', 'request_id',
    )

    lab_blood_ids = fields.One2many(
        'ir.lab_test_blood', 'lab_id',
    )

    doctors_id = fields.Many2one(
        'hr.doctor',
        default=lambda self: self.current_user(),
        readonly=True,
    )

    timezone = pytz.timezone("Asia/Bangkok")
    now = datetime.now(tz=timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M")

    def current_user(self):
        doctors = self.env['hr.doctor'].search([])
        for doctor in doctors:
            if doctor.DT_name == self.env.user:
                return doctor.id

    @api.model
    def create(self, vals):
        if vals.get("lab_seq", "New") == "New":
            vals["lab_seq"] = (
                self.env["ir.sequence"].next_by_code(
                    "lab.request.sequence") or "New"
            )
        result = super(Lab, self).create(vals)
        return result

    def create_by_doctor(self):
        users = self.env["res.users"].search([])
        for user in users:
            user_create = self.env.user
            if user == user_create:
                user_id = user_create.partner_id
        return user_id.name

    @api.depends('lab_state')
    def cumpute_auto_date(self):
        for rec in self:
            if rec.lab_state == 'test':
                rec.lab_date = fields.Date.today()

            if rec.lab_state == 'draft':
                rec.lab_date = ''

    @api.depends('lab_state')
    def cumpute_auto_date_end(self):
        for rec in self:
            if rec.lab_state == 'complate':
                rec.lab_date_end = fields.Date.today()
            else:
                rec.lab_date_end = ''

    def button_test(self):
        self.lab_state = "test"

    def button_complate(self):
        for rec in self:
            if rec.lab_type == 'tb test':
                if not rec.lab_tests.lab_diagnosticresults:
                    raise ValidationError(_("Plase add imagie test"))
                self.lab_state = "complate"
            else:
                if not rec.lab_blood_ids.lab_blood_range:
                    raise ValidationError(_("Plase add Blood Test"))
                self.lab_state = "complate"

    def button_invoice(self):
        self.lab_state = "invoice"

    def button_draft(self):
        self.lab_state = "draft"
        for rec in self:
            rec.lab_tests = [(5, 0, 0)]
            rec.lab_blood_ids = [(5, 0, 0)]

    def unlink(self):
        if self.lab_state in ('test', 'invoice', 'complate'):
            raise ValidationError(
                _(f"Can't Delete Lab {self.patient_id.PT_name} In State {self.lab_state}"))
        else:
            return super(Lab, self).unlink()

    @api.onchange('lab_type')
    def _onchange_lab_type(self):
        for rec in self:
            if rec.lab_type == 'tb test':
                rec.lab_tests = [(5, 0, 0)]

            if rec.lab_type == 'blood test':
                rec.lab_blood_ids = [(5, 0, 0)]

    @api.constrains('lab_type')
    def _check_lab_type_unique(self):
        lab_type_count = self.search_count(
            [
                ('patient_id', '=', self.patient_id.PT_name),
                ('lab_type', '=', self.lab_type),
                ('id', '!=', self.id)
            ]
        )
        if lab_type_count > 0:
            raise ValidationError(_("Lab Type already exists !"))
