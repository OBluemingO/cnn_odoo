from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class IRappointment(models.Model):
    _name = "ir.appointment"
    _rec_name = 'appointment_seq'

    appointment_seq = fields.Char(
        string="Appointment Number",
        readonly=True,
        required=True,
        copy=False,
        default="New"
    )

    patient_id = fields.Many2one(
        "hr.patient",
        required=True,
    )

    lab_id = fields.Many2one('ir.lab')

    medicate_id = fields.Many2one(
        'ir.medicate',
        required=True,
    )

    medicate_seq = fields.Char(
        related='medicate_id.medicate_seq'
    )

    appointment_date = fields.Date(
        string='Appointment Date',
        related='medicate_id.date_appointment_medicate'
    )

    medicate_dispent_count = fields.Integer(
        related='medicate_id.medicate_dispent_count'
    )

    appointment_comment = fields.Text(
        string='Comment',
        required=True,
    )

    doctors_id = fields.Many2one(
        'hr.doctor',
        default=lambda self: self.current_user(),
        readonly=True,
    )


    @api.onchange('patient_id')
    def _onchange_domain_medicate(self):
        for rec in self:
            return {'domain': {'medicate_id': [('patient_id', '=', rec.patient_id.id)]}}

    @api.constrains('medicate_id')
    def _check_medicate_unique(self):
        patient_count = self.search_count(
            [('medicate_id.medicate_seq', '=', self.medicate_seq), ('id', '!=', self.id)]
        )
        if patient_count > 0:
            raise ValidationError(
                _(f"Medicate Sequence {self.medicate_seq} Already Exists !"))

    def current_user(self):
        doctors = self.env['hr.doctor'].search([])
        for doctor in doctors:
            if doctor.DT_name == self.env.user:
                return doctor.id
    
    @ api.model
    def create(self, vals):
        if vals.get("appointment_seq", "New") == "New":
            vals["appointment_seq"] = (
                self.env["ir.sequence"].next_by_code(
                    "appointment.sequence") or "New"
            )
        result = super(IRappointment, self).create(vals)
        return result