from odoo import models, fields

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient', string='Patient', ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    description = fields.Text(string='Description', readonly=True)