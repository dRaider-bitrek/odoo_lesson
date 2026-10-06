from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _order = 'name'
    _inherit = 'hr.hospital.medic.info'

    name = fields.Char(string='Doctor Name', required=True, index=True)
    category_id = fields.Many2one('hospital.doctor.category', string='Category')
    user_id = fields.Many2one('res.users', string='User')
    is_intern = fields.Boolean(compute='_compute_is_intern', store=True)

    observing_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Observing Doctor',
        domain="[('is_intern', '=', False), ('id', '!=', id)]",
    )

    @api.depends('category_id.is_intern_category')
    def _compute_is_intern(self):
        """Derive the intern flag from the doctor's category.

        An alternative is to compare the category with a fixed record found by
        its XML id, but that breaks as soon as the record is deleted or
        duplicated. A boolean on the category keeps the rule configurable and
        lets is_intern be stored and used in domains.
        """
        for record in self:
            record.is_intern = record.category_id.is_intern_category

    @api.constrains('observing_doctor_id')
    def _check_observing_doctor_is_not_intern(self):
        for record in self:
            if record.observing_doctor_id.is_intern:
                raise ValidationError(
                    self.env._('Observing doctor cannot be an intern.'),
                )
