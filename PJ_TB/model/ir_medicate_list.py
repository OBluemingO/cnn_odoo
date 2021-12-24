from odoo import models, fields, api, _


class IRmedicatelist(models.Model):
    _name = "ir.medicate_list"
    _rec_name = "medicament"

    medicate_id = fields.Many2one("ir.medicate")
    # TODO: add infomation about history medicate and display data by using many2one
    # medicate_history_id = fields.Many2one("ir.medicate_history")
    # prescription_id = fields.Many2one("ir.prescription")

    medicament = fields.Selection(
        [
            ("isoniazid", "Isoniazid"),
            ("rifampicin", "Rifampicin"),
            ("pyrazinamide", "Pyrazinamide"),
            ("ethambutol", "Ethambutol"),
            ("isoniazid and rifampicin", "Isoniazid and Rifampicin"),
        ],
        default="isoniazid",
        required=True,
    )

    quantity = fields.Integer(size=10)

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
