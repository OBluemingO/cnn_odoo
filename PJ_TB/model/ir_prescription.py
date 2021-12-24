from odoo import models, fields, api


class IRprescription(models.Model):
    _name = "ir.prescription"

    patient_id = fields.Many2one("hr.patient")
