from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Hospital Disease'
    _order = 'name'
    _parent_store = True

    name = fields.Char(required=True, index=True)
    description = fields.Text()
    parent_id = fields.Many2one(
        'hr.hospital.disease',
        string='Parent Disease',
        ondelete='restrict',
        index=True,
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('hr.hospital.disease', 'parent_id', string='Child Diseases')

    display_name = fields.Char(recursive=True)

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for record in self:
            if record.parent_id:
                record.display_name = f'{record.parent_id.display_name} / {record.name}'
            else:
                record.display_name = record.name

    @api.constrains('parent_id')
    def _check_disease_hierarchy(self):
        if self._has_cycle():
            raise ValidationError(
                self.env._('A disease cannot be a parent of itself or one of its descendants.'),
            )
