{
    'name': 'OIG Contribution Management',
    'version': '1.0',
    'author': 'Echo Technology',
    'category': 'Custom',
    'summary': 'Manage agents, customers, services, and commissions.',
    'depends': ['base', 'account', 'contacts', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/agent_sequence.xml',
        'data/customer_sequence.xml',
        'data/sequence.xml',  # Ensure correct ordering
        'data/scheduled_actions.xml',
        'views/agent_view.xml',
        'views/customer_view.xml',
        'views/service_view.xml',
        'views/contribution_view.xml',  # Ensure it's under 'views/' if applicable
        'views/region_view.xml',
        'reports/report_templates.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'installable': True,
    'application': True,
}
