from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz


class Report_PatientWizard(models.TransientModel):

  _name = "report.patient.wizard"
  _description = "create report patient wizard"

  patient_id = fields.Many2one('hr.patient',
    string='Patient',  
    required=True
  )
  laboratory_id = fields.Many2one('ir.lab', string='Laboratory sequence')
  medicate_id = fields.Many2one('ir.medicate', string='Medicate sequence')

  report_select = fields.Selection(
    [
    ('appoint', 'Appointment Report'),
    ('lab', 'Laboratory Report'),
    ('med', 'Medicate Invoice'),
    ], 
  string='Report Select',
  required=True
  )

  @api.onchange('patient_id','report_select')
  def _onchange_domain_appointment(self):
    for rec in self:
        if rec.report_select:
          if rec.report_select == 'lab':
            return {'domain': {'laboratory_id': [('patient_id', '=', rec.patient_id.id)]}}
          if rec.report_select == 'med':
            return {'domain': {'medicate_id': [('patient_id', '=', rec.patient_id.id)]}}
        else:
          rec.laboratory_id = False
          rec.medicate_id = False

  def print_report(self):
    if self.report_select == 'med':
      if self.medicate_id:
        medicate_data = self.env['ir.medicate'].search([('patient_id', '=', self.patient_id.id)],limit=1)
        ref_template = self.env.ref('PJ_TB.report_medicate_appointment')
        report_action =  ref_template.report_action(medicate_data)
        report_action['close_on_report_download']=True
        return report_action
      else:
        raise ValidationError(_('Plases Select Medicate Sequence !'))

    if self.report_select == 'lab':
      if not self.laboratory_id:
        lab_data = self.env['ir.lab'].search([('patient_id', '=', self.patient_id.id)],limit=1)
        ref_template = self.env.ref('PJ_TB.action_report_lab') 
        report_action = ref_template.report_action(lab_data)
        report_action['close_on_report_download']=True
        return report_action
      else:
        lab_data = self.env['ir.lab'].search([('lab_seq', '=', self.laboratory_id.lab_seq)],limit=1)
        ref_template = self.env.ref('PJ_TB.action_report_detail_lab') 
        report_action = ref_template.report_action(lab_data)
        report_action['close_on_report_download']=True
        return report_action

    if self.report_select == 'appoint':
      appointment_data = self.env['hr.patient'].search([('id', '=', self.patient_id.id)],limit=1)
      ref_template = self.env.ref('PJ_TB.action_report_appointment') 
      report_action = ref_template.report_action(appointment_data)
      report_action['close_on_report_download']=True
      return report_action
