from odoo import fields, models
from odoo.exceptions import UserError


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Patient Visit'
    _order = 'scheduled_datetime desc, id desc'

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
    )
    scheduled_datetime = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
        string='Scheduled Date and Time',
    )
    actual_datetime = fields.Datetime(string='Actual Date and Time')
    patient_id = fields.Many2one('hr.hospital.patient', required=True, string='Patient')
    doctor_id = fields.Many2one('hr.hospital.doctor', required=True, string='Doctor')
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')
    summary = fields.Html(string='Summary')
    active = fields.Boolean(default=True)

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
