from odoo import models
from odoo import fields
from odoo import api
from odoo.exceptions import UserError

PRIORITIES = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Urgente')]

class LibroReclamaciones(models.Model):
    _name = 'libro.reclamaciones' # Libro de Reclamaciones
    _description = 'Libro de Reclamaciones'
    name = fields.Char(string="Código")
    
    state = fields.Selection(
        string="Estado", 
        selection=[('new', 'Nuevo'), ('in_process', 'En Progreso'), ('cancel', 'Cancelado'), ('resolved', 'Resuelto')], 
        default='new',
        track_visibility='onchange'  # Esto ayuda a rastrear cambios
    )
    priority = fields.Selection(string="Prioridad", selection=PRIORITIES, default='1')
    company_id = fields.Many2one('res.company', string="Empresa", default=lambda r:r.env.company.id)
    claim_user_id = fields.Many2one('res.users', string="Responsable")
    
    # IDENTIFIACION DEL CONSUMIDOR RECLAMANTE
    consumer_type = fields.Selection(selection=[('individual', 'Persona Natural'), ('company', 'Persona Jurídica')], string="Tipo de Consumidor", default='individual')
    consumer_company_name = fields.Char(string="Razón Social")
    consumer_company_document = fields.Char(string="N° R.U.C")
    consumer_name = fields.Char(string="Nombres")
    consumer_lastname = fields.Char(string="Apellidos")
    consume_email = fields.Char(string="Correo Electrónico")
    consumer_document_type = fields.Selection(selection=[('1', 'DNI'), ('4','C.E.'), ('7','Pasaporte')], string="Tipo de Documento", default='1')
    consumer_document = fields.Char(string="Número de Documento")
    consumer_phone = fields.Char(string="Número de Teléfono")
    consumer_address = fields.Char(string="Dirección")
    consumer_country_id = fields.Many2one('res.country', string="País", default=lambda r:r.env.ref('base.pe', raise_if_not_found=False).id)
    consumer_state_id = fields.Many2one('res.country.state', string="Departamento")
    consumer_province_id = fields.Many2one('res.city', string="Provincias")
    consumer_district_id = fields.Many2one('l10n_pe.res.city.district', string="Distrito")
    
    # DATOS DEL PADRE, MADRE O TUTOR
    consumer_younger = fields.Boolean(string="Es menor de edad?", default=False)
    consumer_younger_parent_name = fields.Char(string="Nombres")
    consumer_younger_parent_lastname = fields.Char(string="Apellidos")
    consumer_younger_parent_document_type = fields.Selection(selection=[('1', 'DNI'), ('4','C.E.'), ('7','Pasaporte')], string="Tipo de Documento", default='1')
    consumer_younger_parent_document = fields.Char(string="Número de Documento")

    # IDENTIFICACION DEL BIEN CONTRATADO
    product_type = fields.Selection(selection=[('service', 'Servicio'), ('product', 'Producto')], string="Tipo de Producto", default='product')
    product_id = fields.Char(string="Codigo de producto")
    product_name = fields.Char(string="Nombre del producto")
    date_order = fields.Date(string="Fecha de venta")
    order_name = fields.Char(string="Número de orden de venta")
    
    # DETALLE DEL RECLAMO O QUEJA
    claim_type = fields.Selection(selection=[('claim', 'Reclamo'), ('complaint', 'Queja')], string="Tipo de Reclamo", default='claim')
    claim_amount = fields.Float(string="Monto del reclamo",digit=(12,2))
    claim_detail = fields.Text(string="Detalle del reclamo")
    claim_request = fields.Text(string="Solicitud del reclamo")
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda r: r.env.company.currency_id.id)
   
    @api.model_create_multi
    def create(self, vals):
        result = super(LibroReclamaciones, self).create(vals)
        code = "seq.libro.reclamaciones"
        sequence = self.env['ir.sequence'].search([('code', '=', code),('company_id','=',self.env.company.id)], limit=1)
        if not sequence.exists():
            sequence = self.env['ir.sequence'].create({
                'name': 'Secuencia de reclamcion LR',
                'implementation': 'no_gap',
                'prefix': 'LR',
                'padding': 5,
                'use_date_range': False,
                'number_increment': 1,
                'code': code,
                'company_id': self.env.company.id,
            })
        name = sequence.next_by_id()
        result.write({'name': name})
        # Flush para asegurar que se escriba en BD antes de retornar
        result._flush()
        return result
    
    def action_in_process(self):
        if not self.env.user.has_group('l10n_pe_libro_reclamaciones.res_groups_libro_reclamaciones_user'):
            raise UserError("No tienes permisos para cambiar el estado a En Progreso")
        
        """Cambiar estado a En Progreso"""
        if self.state != 'new':
            raise UserError("Para pasar el reclamo en proceso, su estado debe ser Nuevo")
        
        # Escribir el cambio
        self.write({'state': 'in_process'})
        
        # Flush para asegurar que se escriba en BD
        self._flush()
        
        # Invalidar caché para forzar lectura desde BD
        self._invalidate_cache()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
   
    def action_revert(self):
        """Revertir de Cancelado a En Progreso"""
        if not self.env.user.has_group('l10n_pe_libro_reclamaciones.res_groups_libro_reclamaciones_admin'):
            raise UserError("No tienes permisos para revertir el estado del reclamo")
        
        if self.state != 'cancel':
            raise UserError("Para revertir el reclamo a En Proceso, su estado debe ser Cancelado")
        
        self.write({'state': 'in_process'})
        self._flush()
        self._invalidate_cache()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
   
    def action_claim_cancel(self):
        """Cancelar el reclamo"""
        if not self.env.user.has_group('l10n_pe_libro_reclamaciones.res_groups_libro_reclamaciones_admin'):
            raise UserError("No tienes permisos para cancelar el reclamo")
        
        if self.state not in ['new', 'in_process']:
            raise UserError("Para cancelar el reclamo, su estado debe ser Nuevo o En Proceso")
        
        self.write({'state': 'cancel'})
        self._flush()
        self._invalidate_cache()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
   
    def action_claim_resolved(self):
        """Marcar reclamo como resuelto"""
        if not self.env.user.has_group('l10n_pe_libro_reclamaciones.res_groups_libro_reclamaciones_admin'):
            raise UserError("No tienes permisos para resolver el reclamo")
        
        if self.state == 'resolved':
            raise UserError("El reclamo ya se encuentra resuelto")
       
        if self.state != 'in_process':
            raise UserError("Para resolver el reclamo, su estado debe ser En Proceso")
        
        self.write({'state': 'resolved'})
        self._flush()
        self._invalidate_cache()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }