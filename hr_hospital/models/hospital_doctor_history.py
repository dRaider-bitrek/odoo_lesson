from odoo import api, fields, models


class HospitalDoctorHistory(models.Model):
    _name = 'hospital.doctor.history'
    _description = 'Hospital Personal Doctor History'
    _order = 'assignment_date desc, id desc'
    _rec_names_search = ['patient_id', 'doctor_id']

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        required=True,
        ondelete='cascade',
        string='Patient',
    )
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        required=True,
        ondelete='restrict',
        string='Doctor',
    )
    assignment_date = fields.Date(
        required=True,
        default=fields.Date.today,
        string='Assignment Date',
    )
    change_date = fields.Date(string='Doctor Change Date')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('patient_id.name', 'doctor_id.name', 'doctor_id.category_id.name', 'assignment_date')
    def _compute_display_name(self):
        for record in self:
            category_name = record.doctor_id.category_id.name or ''
            assignment_date = fields.Date.to_string(record.assignment_date) or ''
            record.display_name = self.env._(
        '%(patient)s - %(doctor)s (%(category)s) %(assignment_date)s',
                patient=record.patient_id.name or '',
                doctor=record.doctor_id.name or '',
                category=category_name,
                assignment_date=assignment_date,
    )

    @api.onchange('assignment_date', 'change_date')
    def _onchange_change_date(self):
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            return {
                'warning': {
                    'title': self.env._('Invalid doctor change date'),
                    'message': self.env._(
                        'Дата зміни лікаря не може бути раніше ніж дата призначення',
                    ),
                },
            }
        return None
