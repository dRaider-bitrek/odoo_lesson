from odoo import fields,models

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _order = 'name'
    _inherit = 'hr.hospital.medic.info'

    name = fields.Char(string='Patient Name',required=True,index=True)

    doctor_id = fields.Many2one('hr.hospital.doctor',string='Doctor')
    disease_id= fields.Many2one('hr.hospital.disease', string='Disease')
    insurance_policy_number = fields.Char(size=20, string='Insurance Policy Number')
    doctor_history_ids = fields.One2many(
        'hospital.doctor.history',
        'patient_id',
        string='Personal Doctor History',
    )
