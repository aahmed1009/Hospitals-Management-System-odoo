{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage Patients in HMS',
       'author': 'Alaa Ahmed',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/patient_report.xml',  
        'views/hms_patient_views.xml',
        'views/hms_doctor_views.xml',
        'views/hms_department_views.xml',
        'views/res_partner_views.xml'
    ],
    'installable': True,
    'application': True,
}