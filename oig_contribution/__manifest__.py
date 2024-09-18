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
        'data/customer_sequence.xml',  # Include the sequence here
        'data/scheduled_actions.xml',
        'views/customer_view.xml',
        'views/agent_view.xml',
        'views/contribution_view.xml',
        'security/ir.model.access.csv',
        'reports/report_templates.xml',
    ],
    'installable': True,
    'application': True,  # Set this to True if it's a main application
    'auto_install': False,
}

