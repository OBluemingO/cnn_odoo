from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Report_DoctorWizard(models.TransientModel):

  _name = "report.doctor.wizard"
  _description = "create report doctor wizard"

  doctor_id = fields.Many2one('hr.doctor',
    string='Doctor',  
    required=True
  )

  def print_doctor_report(self):
    medicate_data = self.env['hr.doctor'].search([('id', '=', self.doctor_id.id)],limit=1)
    ref_template = self.env.ref('PJ_TB.action_report_doctor')
    return ref_template.report_action(medicate_data)

