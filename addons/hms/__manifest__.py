{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage Patients in HMS',
    'author': 'Alaa Ahmed',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        
    ],
    'installable': True,
    'application': True,
}
