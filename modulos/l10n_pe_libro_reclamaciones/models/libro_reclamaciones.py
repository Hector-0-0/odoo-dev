from odoo import models, fields

PRIORITIES = [('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')]

class LibroReclamaciones(models.Model):
    _name = 'libro.reclamaciones' # Libro de Reclamaciones
    
    name = fields.Char(string="Código")
    
    state = fields.Selection(string="Estado", selection=[('new', 'Nuevo'), ('in_progress', 'En Progreso'), ('cancel', 'Cancelado'), ('resolved', 'Resuelto')], default='new')
    
    priority = fields.Selection(string="Prioridad", selection=PRIORITIES, default='medium')
    
    company_id = fields.Many2one('res.company', string="Empresa")
    
    claim_user_id = fields.Many2one('res.users', string="Responsable")
    
    