from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError
import re


class HrPatient(models.Model):

    _name = "hr.patient"
    _rec_name = "PT_name"
    _description = " detail about patient"

    # general information
    PT_name = fields.Char(
        string="Name",
        required=True
    )

    PT_id_card = fields.Char(
        string="ID Card",
        size=13,
        required=True,
    )

    PT_tel = fields.Char(
        required=True,
        string="Phone",
        size=10,
    )

    PT_email = fields.Char(string="Email")

    PT_address = fields.Text(string="Address")

    PT_gender = fields.Selection(
        [
            ("ชาย", "ชาย"),
            ("หญิง", "หญิง"),
            ("อื่นๆ", "อื่นๆ"),
        ],
        string="Gender",
        default="ชาย",
        required=True
    )

    PT_age = fields.Integer(
        string="Age",
        readonly=True
    )

    PT_birthday = fields.Date(
        string="Birthday", required=True
    )

    # critical information
    PT_congenital_disease = fields.Char(string="Congenital Disease")

    PT_allergy = fields.Char(string="Allergy")

    PT_blood = fields.Selection(
        selection=[
            ("a", "A"),
            ("b", "B"),
            ("ab", "AB"),
            ("o", "O"),
        ],
        string="Blood type",
        default="a",
    )

    lab_requsets = fields.One2many("ir.lab", "patient_id")
    medicates = fields.One2many("ir.medicate", "patient_id", readonly=True)
    patient_main_lines = fields.One2many(
        "hr.patient.line", "relation_id", readonly=True
    )

    @api.constrains("PT_age")
    def _check_age(self):
        if self.PT_age > 100:
            raise UserError(
                "Your age is not correct age should between 0 - 100")

    @api.onchange('PT_birthday')
    def calculate_age(self):
        today = date.today()
        try:
            self.PT_age = today.year - self.PT_birthday.year - \
                ((today.month, today.day) <
                 (self.PT_birthday.month, self.PT_birthday.day))
        except Exception:
            pass

    @api.constrains('PT_tel')
    def check_character_phone(self):
        pattren = r'[\D]+'
        character = re.match(pattren, self.PT_tel)
        if character:
            raise UserError(
                _('Phone Number Invaild'))

    @api.constrains('PT_id_card')
    def check_Id_card(self):
        pattren = r'[\D]+'
        character = re.match(pattren, self.PT_id_card)
        if character:
            raise UserError(
                _('Identity Document Invaild'))

    @api.constrains('PT_id_card')
    def check_Id_card_len(self):
        if len(self.PT_id_card) < 13:
            raise UserError(
                _('Identity Document Invaild'))


class HrPatient_Line(models.Model):

    _name = "hr.patient.line"

    relation_id = fields.Many2one('hr.patient')
    labs_id = fields.Many2one('ir.lab')

    lab_seq = fields.Char(
        related='labs_id.lab_seq'
    )

    lab_type = fields.Selection(
        related='labs_id.lab_type'
    )

    lab_doctor = fields.Char(
        related='labs_id.lab_doctor'
    )

    lab_date = fields.Char(
        related='labs_id.lab_date'
    )

    lab_insurance = fields.Boolean(
        related='labs_id.lab_insurance'
    )

    lab_state = fields.Selection(
        related='labs_id.lab_state'
    )
