from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email address must be unique.')
    ]

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True, readonly=True)
    history = fields.Html(string='History')
    show_history = fields.Boolean(compute="_compute_show_history")
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')
    ], string="Blood Type")
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    email = fields.Char(string='Email')  # ➕ Added field
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', string='State')

    department_id = fields.Many2one('hms.department', string="Department")
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Logs")
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)

    @api.depends('age')
    def _compute_show_history(self):
        for rec in self:
            rec.show_history = rec.age and rec.age >= 50

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Auto-Checked",
                    'message': "PCR has been automatically checked because age is under 30."
                }
            }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id and not self.department_id.is_opened:
            self.department_id = False
            return {
                'warning': {
                    'title': "Closed Department",
                    'message': "You cannot choose a closed department."
                }
            }

    @api.constrains('cr_ratio', 'pcr')
    def _check_cr_ratio_required(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.constrains('email')
    def _check_valid_email(self):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            if record.email and not re.match(pattern, record.email):
                raise ValidationError("Please provide a valid email address.")

    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            log_vals = {
                'description': f"State changed to {self.state}",
                'date': fields.Datetime.now()
            }
            self.log_ids = [(0, 0, log_vals)]
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                born = record.birth_date
                # Calculate age
                record.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                record.age = 0