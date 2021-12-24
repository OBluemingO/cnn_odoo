from odoo import models, fields, api, _

# ? not sure i need this model , maybe can delete it 

class IRmedicatehistory(models.Model):
    _name = "ir.medicate_history"

    medicate_lists = fields.One2many("ir.medicate_list", "medicate_history_id")
    