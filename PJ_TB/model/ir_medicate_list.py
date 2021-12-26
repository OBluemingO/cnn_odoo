from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class IRmedicatelist(models.Model):
    _name = "ir.medicate_list"
    _rec_name = "medicament"

    medicate_id = fields.Many2one("ir.medicate")
    # prescription_id = fields.Many2one("ir.prescription")

    medicament = fields.Selection(
        [
            ("isoniazid", "Isoniazid"),
            ("rifampicin", "Rifampicin"),
            ("pyrazinamide", "Pyrazinamide"),
            ("ethambutol", "Ethambutol"),
            ("isoniazid and rifampicin", "Isoniazid and Rifampicin"),
        ],
        default="isoniazid and rifampicin",
        required=True,
    )

    quantity = fields.Integer(
        default=1,
        size=10
    )

    dose = fields.Char(required=True)

    treament_duration = fields.Selection(
        [
            ("3 m", "3 months"),
            ("4 m", "4 months"),
            ("6 m", "6 months"),
            ("9 m", "9 months"),
        ],
        string="Treament Duration",
    )

    frequency = fields.Selection(
        [
            ("daily", "Daily"),
            ("once weekly", "Once weekly"),
            ("twice weekly", "Twice weekly"),
        ],
        default="daily",
    )

    unit_price = fields.Float(
        string='Unit price',
        store=True,
        compute='compute_unit_price'
    )

    @api.depends('medicament', 'quantity')
    def compute_unit_price(self):
        for rec in self:
            if rec.quantity:
                if rec.medicament == 'isoniazid':
                    rec.unit_price = 150 * rec.quantity

                if rec.medicament == 'rifampicin':
                    rec.unit_price = 170 * rec.quantity

                if rec.medicament == 'pyrazinamide':
                    rec.unit_price = 120 * rec.quantity

                if rec.medicament == 'ethambutol':
                    rec.unit_price = 100 * rec.quantity

                if rec.medicament == 'isoniazid and rifampicin':
                    rec.unit_price = 200 * rec.quantity
