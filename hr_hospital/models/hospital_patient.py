from odoo import fields, models


class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _order = 'name'
    _inherit = 'hr.hospital.medic.info'

    name = fields.Char(string='Patient Name', required=True, index=True)

    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor')
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')
    insurance_policy_number = fields.Char(size=20, string='Insurance Policy Number')
    doctor_history_ids = fields.One2many(
        'hospital.doctor.history',
        'patient_id',
        string='Personal Doctor History',
    )
    visit_ids = fields.One2many('hr.hospital.visit', 'patient_id', string='Visits')
    visit_count = fields.Integer(compute='_compute_visit_count')

    def _compute_visit_count(self):
        visit_data = self.env['hr.hospital.visit']._read_group(
            [('patient_id', 'in', self.ids)],
            ['patient_id'],
            ['__count'],
        )
        counts = {patient.id: count for patient, count in visit_data}
        for patient in self:
            patient.visit_count = counts.get(patient.id, 0)

    def action_open_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Patient Visits'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('New Patient Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
                'default_disease_id': self.disease_id.id,
            },
        }
