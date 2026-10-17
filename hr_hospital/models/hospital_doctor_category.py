from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    _name = "hospital.doctor.category"
    _description = "Hospital Doctor Qualification"
    _order = "sequence, name"

    name = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)
    is_intern_category = fields.Boolean(default=False, string="Intern Category")
    doctor_ids = fields.One2many(
        'hr.hospital.doctor',
        'category_id',
        string="Doctors",
    )
    _name_uniq = models.Constraint(
        'unique (name)',
        'Назва кваліфікації вже існує!',
    )
