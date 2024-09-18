# __manifest__.py
{
    'name': 'OIG Contribution',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for OIG Contributions',
    'depends': ['base'],
    'data': [
        'views/commission_views.xml',
        'data/models.xml',
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
    ],
    'installable': True,
    'application': True,  # Set this to True if it's a main application
    'auto_install': False,
}

