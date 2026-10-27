from odoo.exceptions import ValidationError

from odoo import api, fields, models


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _order = 'name'
    _inherit = 'hr.hospital.medic.info'

    name = fields.Char(string='Doctor Name', required=True, index=True)
    category_id = fields.Many2one('hospital.doctor.category', string='Category')
    user_id = fields.Many2one('res.users', string='User')
    active = fields.Boolean(default=True)
    patient_ids = fields.One2many(
        'hr.hospital.patient',
        'doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        'hr.hospital.visit',
        'doctor_id',
        string='Visits',
    )
    is_intern = fields.Boolean(compute='_compute_is_intern', store=True)

    observing_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Observing Doctor',
        domain="[('is_intern', '=', False), ('id', '!=', id)]",
    )
    intern_ids = fields.One2many(
        'hr.hospital.doctor',
        'observing_doctor_id',
        string='Interns',
    )
    intern_count = fields.Integer(compute='_compute_intern_count')

    def _compute_intern_count(self):
        for doctor in self:
            doctor.intern_count = len(doctor.intern_ids)

    def action_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('New Patient Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }

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
