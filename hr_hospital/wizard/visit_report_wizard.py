from datetime import datetime, time

from odoo import Command, api, fields, models
from odoo.fields import Domain


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Patient Visit Report'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    patient_ids = fields.Many2many('hr.hospital.patient', string='Patients')
    date_from = fields.Date(string='Period Start')
    date_to = fields.Date(string='Period End')
    completed_only = fields.Boolean(string='Completed Visits Only')
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            values['doctor_ids'] = [Command.set(active_ids)]
        elif active_model == 'hr.hospital.patient' and 'patient_ids' in fields_list:
            values['patient_ids'] = [Command.set(active_ids)]
        return values

    def action_open_visits(self):
        self.ensure_one()
        domain = Domain.TRUE
        if self.doctor_ids:
            domain &= Domain('doctor_id', 'in', self.doctor_ids.ids)
        if self.patient_ids:
            domain &= Domain('patient_id', 'in', self.patient_ids.ids)
        if self.date_from:
            domain &= Domain(
                'scheduled_datetime',
                '>=',
                datetime.combine(self.date_from, time.min),
            )
        if self.date_to:
            domain &= Domain(
                'scheduled_datetime',
                '<=',
                datetime.combine(self.date_to, time.max),
            )
        if self.completed_only:
            domain &= Domain('state', '=', 'completed')
        if self.disease_id:
            domain &= Domain('disease_id', '=', self.disease_id.id)
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Patient Visits'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': list(domain),
        }
