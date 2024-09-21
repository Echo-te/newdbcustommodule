{
    'name': 'OIG Contributions',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage daily contributions for OIG multiventures',
    'description': """
    This module manages the daily contributions collection process for OIG multiventures.
    It includes functionality for agents, customers, services, contributions, and commissions.
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/menu_views.xml',
        'views/agent_views.xml',
        'views/customer_views.xml',
        'views/service_views.xml',
        'views/commission_views.xml',
        'views/region_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
