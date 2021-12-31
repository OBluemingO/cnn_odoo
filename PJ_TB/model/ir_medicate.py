from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class IRmedicate(models.Model):
    _name = "ir.medicate"
    _rec_name = "medicate_seq"

    patient_id = fields.Many2one(
        "hr.patient",
        required=True,
    )
    prescription_id = fields.Many2one("ir.prescription")
    medicate_lists = fields.One2many("ir.medicate_list", "medicate_id")
    appointment_ids = fields.One2many("ir.appointment", "medicate_id")

    patient_name = fields.Char(
        related='patient_id.PT_name'
    )

    medicate_seq = fields.Char(
        string="Dispent Number",
        readonly=True,
        required=True,
        copy=False,
        default="New"
    )

    date_dispensing = fields.Date(
        string="Date Dispensing",
        default=fields.Date.today(),
        readonly=True
    )

    date_appointment_medicate = fields.Date(
        string="Date appointment Medicate",
        required=True,
    )

    pharmacy = fields.Many2one(
        "res.partner",
        required=True,
    )

    medicate_state = fields.Selection(
        [
            ("blank", "Not specified or presumably full quantity of prescription"),
            ("p", "Partial fill"),
            ("c", "Completion of partial fill"),
        ],
        string="Medicate State",
        required=True,
    )

    medicate_dispent_count = fields.Integer(
        string="Dispent Count",
        readonly=True,
    )

    medicate_total = fields.Float(
        string='Total Amount',
        store=True,
        compute="compute_total_amount",
    )

    @api.constrains("medicate_dispent_count")
    def _check_dispent_count(self):
        for rec in self:
            if rec.medicate_dispent_count == 0:
                raise UserError(_("Dispent count can't be '0'"))

    @api.model
    def create(self, vals):
        if vals.get("medicate_seq", "New") == "New":
            vals["medicate_seq"] = (
                self.env["ir.sequence"].next_by_code(
                    "medicate.sequence") or "New"
            )
        result = super(IRmedicate, self).create(vals)
        return result

    @api.onchange('patient_id')
    def onchange_count_patient(self):
        medicate = self.env['ir.medicate'].search_count(
            [('patient_id', '=', self.patient_id.id)])

        self.medicate_dispent_count = medicate+1

    @api.depends('medicate_lists.unit_price')
    def compute_total_amount(self):
        totals = 0
        for rec in self:
            for total in rec.medicate_lists:
                totals += total.unit_price
            rec.medicate_total = totals

    @api.constrains('date_appointment_medicate')
    def _check_create_and_vaild_date_appointment(self):
        for rec in self:
            list_appointment = rec.env['ir.medicate'].search(
                [('patient_name', '=', rec.patient_name)]
            )

            if self.date_appointment_medicate < date.today() or self.date_appointment_medicate == date.today():
                raise ValidationError(_("Date Appointment Invaild"))

            if len(list_appointment) > 1:
                date_point = list_appointment[-2].date_appointment_medicate
                date_today = list_appointment[-1].date_appointment_medicate
                if date_point <= date_today:
                    raise ValidationError(
                        _("Can't Create Medicate Because Before Medicate It's Not Time Yet"))
