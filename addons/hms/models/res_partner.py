from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        tracking=True
    )

    tax_id = fields.Char(
        string='Tax ID',
        tracking=True
    )

    _sql_constraints = [
        ('email_uniq', 'UNIQUE(email)', 'Email must be unique.'),
        ('tax_id_uniq', 'UNIQUE(tax_id)', 'Tax ID must be unique.')
    ]

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self.filtered('email'):
            existing = self.search([
                ('email', '=', rec.email),
                ('id', '!=', rec.id)
            ], limit=1)
            if existing:
                raise ValidationError(f"Email '{rec.email}' is already used by {existing.name}.")

    @api.constrains('related_patient_id')
    def _check_unique_patient_email(self):
        for rec in self.filtered('related_patient_id'):
            patient_email = (rec.related_patient_id.email or '').strip().lower()
            if patient_email:
                duplicate = self.search([
                    ('id', '!=', rec.id),
                    ('related_patient_id.email', '=', patient_email)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        f"The patient email '{patient_email}' is already linked to another customer: '{duplicate.name}'."
                    )

    @api.constrains('tax_id')
    def _check_tax_id_required(self):
        for rec in self:
            if rec.is_company and not rec.tax_id:
                raise ValidationError("Tax ID is required for companies.")

    @api.constrains('tax_id')
    def _check_tax_id_format(self):
        for rec in self.filtered('tax_id'):
            if len(rec.tax_id.strip()) < 3:
                raise ValidationError("Tax ID must be at least 3 characters.")

    def unlink(self):
        protected = self.filtered('related_patient_id')
        if protected:
            raise ValidationError(
                "You cannot delete a customer linked to a patient. Unlink the patient first."
            )
        return super().unlink()
