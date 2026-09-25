from odoo import fields,models

class HospitalDisease(models.Model):
    _name = "hr.hospital.disease"
    _description = 'Disease'
    _order = 'name'

    name = fields.Char(string='Disease',required=True,index=True)
    description = fields.Text(string='Description')
