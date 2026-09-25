from odoo import fields,models

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _order = 'name'

    name = fields.Char(string='Patient Name',required=True,index=True)

    doctor_id = fields.Many2one('hr.hospital.doctor',string='Doctor')
    disease_id= fields.Many2one('hr.hospital.disease', string='Disease')
