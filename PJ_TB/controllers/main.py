from odoo import http
from odoo.http import request


class HospitalController(http.Controller):

    @http.route('/create_patient', auth='public', website=True)
    def patient_form(self, **kw):
        patient_rec = request.env['hr.patient'].sudo().search([])
        return request.render('PJ_TB.form_patient', {'patient_rec': patient_rec})

    @http.route('/create_patient/done', type='http', auth='public', website=True)
    def patient_create(self, **kw):
        return request.render('PJ_TB.form_patient_done', {})

    # @http.route('/appointment', auth='public', website=True)
    # def patient_form(self, **kw):
    #     appointment = request.env['ir.appointment'].sudo().search([])
    #     return request.render({'patient_rec': appointment})
