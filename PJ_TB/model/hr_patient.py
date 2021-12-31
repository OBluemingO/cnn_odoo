from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError
import pytz
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

    PT_member = fields.Selection(
        selection=[
            ("new", "New"),
            ("old", "Old"),
        ],
        string="Patient Member",
        compute='compute_new_patient_today',
    )

    PT_status = fields.Boolean(
        string='Status',
        compute='_compute_status',
        store=True
    )

    laboratory_count = fields.Integer(
        string='Laboratory Count',
        compute='compute_laboratory_count',
    )

    medicate_count = fields.Integer(
        string='Medicate Count',
        compute='compute_medicate_count',
    )

    appointment_count = fields.Integer(
        string='Appointment Count',
        compute='compute_appointment_count',
    )

    lab_requsets = fields.One2many(
        "ir.lab",
        "patient_id",
        readonly=True
    )

    medicates = fields.One2many(
        "ir.medicate",
        "patient_id",
        readonly=True
    )

    appointment = fields.One2many(
        "ir.appointment",
        "patient_id",
        readonly=True
    )

    doctors_id = fields.Many2one(
        'hr.doctor',
        domain=[('DT_status', '=', 'null')],
        required=True,
    )

    @api.constrains('PT_name')
    def _check_name_unique(self):
        patient_count = self.search_count(
            [('PT_name', '=', self.PT_name), ('id', '!=', self.id)]
        )
        if patient_count > 0:
            raise ValidationError(_("patient name already exists !"))

    def compute_new_patient_today(self):
        for rec in self:
            rec.PT_member = 'old'
            create_date = str(rec.create_date).split()
            if create_date[0] == str(date.today()):
                rec.PT_member = 'new'

    def compute_laboratory_count(self):
        for rec in self:
            count = self.env['ir.lab'].search_count(
                [('patient_id', '=', rec.id)])

            if count > 0:
                rec.laboratory_count = count
            else:
                rec.laboratory_count = 0

    def compute_appointment_count(self):
        for rec in self:
            count = self.env['ir.appointment'].search_count(
                [('patient_id', '=', rec.id)])

            if count > 0:
                rec.appointment_count = count
            else:
                rec.appointment_count = 0

    def compute_medicate_count(self):
        for rec in self:
            count = self.env['ir.medicate'].search_count(
                [('patient_id', '=', rec.id)])

            if count > 0:
                rec.medicate_count = count
            else:
                rec.medicate_count = 0

    @api.depends('lab_requsets.lab_state', 'appointment.appointment_date')
    def _compute_status(self):
        timezone = pytz.timezone("Asia/Bangkok")
        now = datetime.now(tz=timezone)
        dt_string = now.strftime("%Y-%m-%d")

        for rec in self:
            rec.PT_status = False
            list_state = rec.env['ir.lab'].search(
                [('patient_id', '=', rec.PT_name)])

            appointments = rec.env['ir.appointment'].search(
                [('patient_id.PT_name', '=', rec.PT_name)])

            if list_state:
                count = 0
                for r in list_state:
                    if r.lab_state == 'complate':
                        count += 1
                if count == len(list_state):
                    rec.PT_status = True
                    if len(appointments) > 1:
                        if appointments[-1].appointment_date != appointments[-2].appointment_date:
                            rec.PT_status = True
                    else:
                        date_appointment = appointments.appointment_date
                        if str(date_appointment) == str(dt_string):
                            rec.PT_status = False

    @api.constrains("PT_age")
    def _check_age(self):
        if self.PT_age > 100:
            raise UserError(
                "Your age is not correct age should between 0 - 100")

        if self.PT_age < 0:
            raise UserError(
                "Your age is not correct age should between 0 - 100")

    @api.onchange('PT_birthday')
    def calculate_age(self):
        today = date.today()
        for rec in self:
            if rec.PT_birthday:
                rec.PT_age = today.year - rec.PT_birthday.year - \
                    ((today.month, today.day) <
                     (rec.PT_birthday.month, rec.PT_birthday.day))

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

    def button_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'res_model': 'ir.appointment',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def button_Laboratory(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Laboratory',
            'res_model': 'ir.lab',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def button_medicate(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medicate',
            'res_model': 'ir.medicate',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
