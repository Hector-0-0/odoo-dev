{
    'name': 'Libro de Reclamaciones',
    'version': '1.0',
    'summary': 'Módulo para gestionar el Libro de Reclamaciones según normativa INDECOPI',
    'author': 'Hector-0-0',
    'description': """
Libro de Reclamaciones
====================
Este módulo permite a las empresas peruanas gestionar el Libro de Reclamaciones de acuerdo con la normativa establecida por el INDECOPI.
Facilita el registro, seguimiento y generación de reportes relacionados con las reclamaciones de los clientes, asegurando el 
cumplimiento legal y mejorando la atención al cliente.
    """,
    'category': 'Other',
    'depends': ['base_setup', 'base', 'mail', 'l10n_pe'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/res_groups.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',
        'views/libro_reclamaciones.xml',
        'views/res_config_settings.xml',
        'report/report.xml',
        'report/report_libro_reclamaciones.xml',
    ],
}
