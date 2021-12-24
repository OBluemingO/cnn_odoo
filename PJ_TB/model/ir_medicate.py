from collections import defaultdict
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IRmedicate(models.Model):
    _name = "ir.medicate"
    _rec_name = "medicate_seq"

    patient_id = fields.Many2one("hr.patient")
    prescription_id = fields.Many2one("ir.prescription")
    medicate_lists = fields.One2many("ir.medicate_list", "medicate_id")

    medicate_seq = fields.Char(
        string="Dispent Number", readonly=True, required=True, copy=False, default="New"
    )

    date_dispensing = fields.Date(
        string="Date Dispensing", default=fields.Date.today())

    date_appointment_medicate = fields.Date(string="Date appointment Medicate")

    pharmacy = fields.Many2one("res.partner")

    medicate_state = fields.Selection(
        [
            ("blank", "Not specified or presumably full quantity of prescription"),
            ("p", "Partial fill"),
            ("c", "Completion of partial fill"),
        ],
        string="Medicate State",
    )

    # compute_dispent_count = fields.Integer(
    #     compute='count_patient',
    #     store=False,
    # )

    medicate_dispent_count = fields.Integer(
        string="Dispent Count",
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
