from odoo import models, fields, api
from datetime import datetime
import pytz


class Lab(models.Model):
    _name = "ir.lab"
    _rec_name = "lab_seq"

    lab_seq = fields.Char(
        string="Lab Number", readonly=True, required=True, copy=False, default="New"
    )

    lab_type = fields.Selection(
        selection=[
            ("skin test", "Skin Test"),
            ("blood test", "Blood Test"),
            ("tb test", "Tubercusius Image Predict"),
        ],
        string="Test Type",
        default="skin test",
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

    # ใบกำกับภาษี
    lab_insurance = fields.Boolean(string="invoice to insurance")

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

    patient_id = fields.Many2one("hr.patient")
    partner_id = fields.Many2one("res.partner")

    patient_relation_lines = fields.One2many(
        'hr.patient.line', 'labs_id'
    )

    lab_tests = fields.One2many(
        'ir.lab_test', 'request_id',
    )

    timezone = pytz.timezone("Asia/Bangkok")
    now = datetime.now(tz=timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M")

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
        self.lab_state = "complate"

    def button_invoice(self):
        self.lab_state = "invoice"

    def button_draft(self):
        self.lab_state = "draft"
