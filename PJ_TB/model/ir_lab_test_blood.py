from odoo import models, fields, api, _
from odoo.exceptions import ValidationError , UserError


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
        string="Blood Range",
        required=True
    )

    lab_blood_diagnosticresults = fields.Selection([
        ('rh', 'polycythemia'),
        ('rl', 'anemia'),
        ('wh', 'Leukocytosis'),
        ('wl', 'Leukopenia'),
    ], 
    string='diagnosticresults',
    compute="_compute_diagnos"
    )

    @api.depends('lab_blood_range','lab_blood_type')
    def _compute_diagnos(self):
        for rec in self:
            rec.lab_blood_diagnosticresults = False
            if rec.lab_blood_range:
                split_text = str(rec.lab_blood_range).split()
                if rec.lab_blood_type == 'r':
                    try:
                        rec.lab_blood_diagnosticresults = 'rl'
                        if int(split_text[0]) > 11000:
                            rec.lab_blood_diagnosticresults = 'rh'
                    except:
                        raise UserError(_('Invalid Input Plases Try Again'))
                else:
                    try:
                        rec.lab_blood_diagnosticresults = 'wl'
                        if int(split_text[0]) > 11000:
                            rec.lab_blood_diagnosticresults = 'wh'
                    except:
                        raise UserError(_('Invalid Input Plases Try Again'))
            

    