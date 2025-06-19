from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        tracking=True,
        index=True
    )

    tax_id = fields.Char(
        string='Tax ID',
        tracking=True,
        index=True
    )

    _sql_constraints = [
        ('email_uniq', 'UNIQUE(email)', 'Email address must be unique!'),
        ('tax_id_uniq', 'UNIQUE(tax_id)', 'Tax ID must be unique!')
    ]

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self.filtered('email'):
            email = rec.email.strip().lower()
            existing = self.search([
                ('id', '!=', rec.id),
                ('email', '=', email)
            ], limit=1)
            if existing:
                raise ValidationError(f"Email '{email}' is already used by {existing.name}.")

    @api.constrains('related_patient_id')
    def _check_unique_patient_email(self):
        for rec in self.filtered('related_patient_id'):
            patient_email = (rec.related_patient_id.email or '').strip().lower()
            if patient_email:
                existing = self.search([
                    ('id', '!=', rec.id),
                    ('related_patient_id.email', '=', patient_email)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        f"The patient email '{patient_email}' is already linked to another customer: {existing.name}"
                    )

    @api.constrains('tax_id')
    def _check_tax_id_required_for_customers(self):
        for rec in self:
            if rec.customer_rank > 0 and not rec.tax_id:
                raise ValidationError("Tax ID is required for customers.")

    @api.constrains('tax_id')
    def _check_tax_id_format(self):
        for rec in self.filtered('tax_id'):
            if len(rec.tax_id.strip()) < 3:
                raise ValidationError("Tax ID must be at least 3 characters long.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(
                    f"You cannot delete customer '{rec.name}' because they are linked to patient '{rec.related_patient_id.name}'."
                )
        return super().unlink()
