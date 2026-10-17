from datetime import datetime, time, timedelta

from odoo import Command, api, fields, models


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Patient Visit Report'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')
    date_from = fields.Date(string='Period Start')
    date_to = fields.Date(string='Period End')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            values['doctor_ids'] = [Command.set(active_ids)]
        return values

    def action_open_visits(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.date_from:
            domain.append((
                'scheduled_datetime',
                '>=',
                datetime.combine(self.date_from, time.min),
            ))
        if self.date_to:
            domain.append((
                'scheduled_datetime',
                '<',
                datetime.combine(self.date_to + timedelta(days=1), time.min),
            ))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Patient Visits'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'group_by': 'disease_id'},
        }
