# Copyright 2021 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Hospital Management',
    'version': '19.0.1.0.0',
    'category': 'Uncategorized',
    'summary': 'Manage hospital doctors, patients, diseases, and visits',
    'author': 'dRaider',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_disease_data.xml',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_views.xml',

    ],
    'demo': [
        'demo/hr_hospital_demo.xml',
    ],
    'images': [
        'custom_addons/odoo_lesson/hr_hospital/static/description/icons8-96.png'
        ],
    'installable': True,
    'application': True,
}