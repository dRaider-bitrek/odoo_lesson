from odoo import api, fields, models
from odoo.exceptions import UserError


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Patient Visit'
    _order = 'scheduled_datetime desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, index=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='planned',
        required=True,
        string='Visit Status',
        tracking=True,
    )
    scheduled_datetime = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
        string='Scheduled Date and Time',
    )
    actual_datetime = fields.Datetime(string='Actual Date and Time')
    patient_id = fields.Many2one('hr.hospital.patient', required=True, string='Patient')
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        required=True,
        string='Doctor',
        tracking=True,
    )
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')
    summary = fields.Html(string='Summary')
    active = fields.Boolean(default=True)
    same_disease_visit_count = fields.Integer(compute='_compute_same_disease_visit_count')

    @api.depends('disease_id')
    def _compute_same_disease_visit_count(self):
        disease_ids = self.mapped('disease_id').ids
        counts = {}
        if disease_ids:
            visit_data = self._read_group(
                [('disease_id', 'in', disease_ids)],
                ['disease_id'],
                ['__count'],
            )
            counts = {disease.id: count for disease, count in visit_data}
        for visit in self:
            visit.same_disease_visit_count = counts.get(visit.disease_id.id, 0)

    def action_open_same_disease_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Patient Visits'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
            'context': {'default_disease_id': self.disease_id.id},
        }

    @api.model
    def _cron_cancel_overdue_visits(self):
        overdue_visits = self.search([
            ('state', '=', 'planned'),
            ('scheduled_datetime', '<', fields.Datetime.now()),
        ])
        overdue_visits.write({'state': 'cancelled'})
        return len(overdue_visits)

    def write(self, vals):
        protected_fields = {'scheduled_datetime', 'actual_datetime', 'doctor_id'}
        if protected_fields.intersection(vals) and self.filtered(
            lambda visit: visit.state == 'completed',
        ):
            raise UserError(
                self.env._(
                    'The date, time, and doctor cannot be changed for a completed visit.',
                ),
            )
        if 'active' in vals and self.filtered(lambda visit: visit.state == 'completed'):
            raise UserError(self.env._('A completed visit cannot be archived.'))
        return super().write(vals)

    def unlink(self):
        if self.env.context.get('_force_unlink'):
            return super().unlink()
        if self.filtered(lambda visit: visit.state == 'completed'):
            raise UserError(self.env._('A completed visit cannot be deleted.'))
        return super().unlink()
