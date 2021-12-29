from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LabTestBlood(models.Model):
    _name = "ir.lab_test_blood"

    lab_id = fields.Many2one('ir.lab')

    lab_blood_type = fields.Selection([
        ('r', 'Red'),
        ('w', 'White'),
    ],
        string='Blood Type',
        required=True
    )

    lab_blood_range = fields.Char(
        string="Blood Range"
    )

    lab_blood_normal = fields.Char(
        string="Blood Normal"
    )
