from odoo import models, fields

PRIORITIES = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Urgente')]

class LibroReclamaciones(models.Model):
    _name = 'libro.reclamaciones' # Libro de Reclamaciones
    _description = 'Libro de Reclamaciones'
    name = fields.Char(string="Código")
    
    state = fields.Selection(string="Estado", selection=[('new', 'Nuevo'), ('in_progress', 'En Progreso'), ('cancel', 'Cancelado'), ('resolved', 'Resuelto')], default='new')
    
    priority = fields.Selection(string="Prioridad", selection=PRIORITIES, default='1')
    
    company_id = fields.Many2one('res.company', string="Empresa", default=lambda r:r.env.company.id)
    
    claim_user_id = fields.Many2one('res.users', string="Responsable")
    
    # IDENTIFIACION DEL CONSUMIDOR RECLAMANTE
    consumer_type = fields.Selection(selection=[('individual', 'Persona Natural'), ('company', 'Persona Jurídica')], string="Tipo de Consumidor", default='individual')
    
    consumer_company_name = fields.Char(string="Razón Social")
    consumer_company_document = fields.Char(string="N. R.U.C")
    
    consumer_name = fields.Char(string="Nombres")
    consumer_lastname = fields.Char(string="Apellidos")
    consume_email = fields.Char(string="Correo Electrónico")
    consumer_document_type = fields.Selection(selection=[('1', 'DNI'), ('4','C.E.'), ('7','Pasaporte')], string="Tipo de Documento", default='1')

    consumer_document = fields.Char(string="Número de Documento")
    consumer_phone = fields.Char(string="Número de Teléfono")
    consumer_address = fields.Char(string="Dirección")
    
    consumer_country_id = fields.Many2one('res.country', string="País", default=lambda r:r.env.ref('base.pe').id)

    consumer_state_id = fields.Many2one('res.country.state', string="Departamento")

    consumer_province_id = fields.Many2one('res.city', string="Provincias")
    
    consumer_district_id = fields.Many2one('l10n_pe.res.city.district', string="Distrito")
    