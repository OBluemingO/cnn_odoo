from odoo import models, fields, api


class IRappointment(models.Model):
    _name = "ir.appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one("hr.patient")
    medicate_id = fields.Many2one("ir.medicate")
    lab_id = fields.Many2one('ir.lab')

    appointment_date = fields.Date(
        related='patient_id.medicates.date_appointment_medicate',
        string='Appointment Date'
    )

    appointment_comment = fields.Text(
        string='Comment'
    )

    appointment_doctor = fields.Char(
        related='patient_id.lab_requsets.lab_doctor',
        string='Doctor'
    )
