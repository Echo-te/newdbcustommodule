# __manifest__.py
{
    'name': 'OIG Contributions Management',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'data/customer_sequence.xml',  # Include the sequence here
        'views/customer_view.xml',
        'views/agent_view.xml',
        'views/contribution_view.xml',
        'reports/report_templates.xml',
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
    ],
}
