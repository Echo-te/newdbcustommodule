# __manifest__.py
{
    'name': 'OIG Contribution',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for OIG Contributions',
    'depends': ['base'],
    'data': [
    'views/menu.xml',
    'views/service_view.xml',
    'views/agent_view.xml',
    'views/customer_view.xml',
    'views/commission_view.xml',
    'views/region_view.xml',
    'security/ir.model.access.csv',
    'data/customer_sequence.xml',
    'data/agent_sequence.xml',
    'data/scheduled_actions.xml',
    'views/menu.xml',
    ],
    'installable': True,
    'application': True,  # Set this to True if it's a main application
    'auto_install': False,
}

