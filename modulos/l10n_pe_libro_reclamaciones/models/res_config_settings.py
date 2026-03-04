from odoo import models
from odoo import fields

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    default_claim_user_id = fields.Many2one('res.users', string="Responsable de reclamos y quejas")
    default_claim_attention_period = fields.Integer(string="Plazo de atención del reclamo", default=15)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    claim_user_id = fields.Many2one('res.users',
                                related='company_id.default_claim_user_id',
                                readonly=False)
    
    claim_attention_period = fields.Integer(related='company_id.default_claim_attention_period',
                                            readonly=False)