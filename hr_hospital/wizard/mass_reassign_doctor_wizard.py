from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Personal Doctor'

    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        required=True,
        string='New Doctor',
    )
    change_date = fields.Date(default=fields.Date.today, string='Change Date')

    def action_reassign_doctor(self):
        self.ensure_one()
        patients = self.env['hr.hospital.patient'].browse(self.env.context.get('active_ids', []))
        patients.write({'doctor_id': self.new_doctor_id.id})
        self.env['hospital.doctor.history'].create(
            [
                {
                    'patient_id': patient.id,
                    'doctor_id': self.new_doctor_id.id,
                    'assignment_date': self.change_date,
                }
                for patient in patients
            ]
        )
        return {'type': 'ir.actions.act_window_close'}
