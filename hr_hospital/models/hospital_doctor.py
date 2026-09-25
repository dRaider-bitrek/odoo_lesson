from odoo import fields, models

class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _order = 'name'

    name = fields.Char(string= 'Doctor Name',required=True,index=True)

    observing_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Observing Doctor',
        domain="[('id', '!=', id)]"
    )