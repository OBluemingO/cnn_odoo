from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class IRappointment(models.Model):
    _name = "ir.appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one("hr.patient")
    lab_id = fields.Many2one('ir.lab')

    appointment_date = fields.Datetime(
        string='Appointment Date',
        required=True,
    )

    appointment_comment = fields.Text(
        string='Comment'
    )

    appointment_doctor = fields.Char(
        default=lambda self: self.create_by_doctor(),
        string='Doctor',
        readonly=True
    )

    @api.constrains('appointment_date')
    def _check_vaild_date_appointment(self):
        if self.appointment_date < self.create_date or self.appointment_date == self.create_date:
            raise ValidationError(_("Date Appointment Invaild"))

    def create_by_doctor(self):
        users = self.env["res.users"].search([])
        for user in users:
            user_create = self.env.user
            if user == user_create:
                user_id = user_create.partner_id
                return user_id.name
