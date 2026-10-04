from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Hospital Medical Information'

    blood_type = fields.Selection(
        selection=[
            ('o_positive', 'O(I) Rh+'),
            ('o_negative', 'O(I) Rh-'),
            ('a_positive', 'A(II) Rh+'),
            ('a_negative', 'A(II) Rh-'),
            ('b_positive', 'B(III) Rh+'),
            ('b_negative', 'B(III) Rh-'),
            ('ab_positive', 'AB(IV) Rh+'),
            ('ab_negative', 'AB(IV) Rh-'),
        ],
        string='Blood Type',
    )
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')],
        string='Gender',
    )
    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(compute='_compute_age', string='Age')

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0
