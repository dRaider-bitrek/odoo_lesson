from odoo import fields,models

class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'
    _order = 'visit_date desc'

    name = fields.Char(string='Visit')
    visit_date = fields.Datetime(string='Visit Date',default=fields.Datetime.now)
    patient_id = fields.Many2one('hr.hospital.patient',string='Patient')
    doctor_id = fields.Many2one('hr.hospital.doctor',string='Doctor')
    disease_id =   fields.Many2one("hr.hospital.disease",string='Disease')
