from openerp.osv import fields, osv

class rdm_customer(osv.osv):    
    _inherit = "rdm.customer"
    _columns = {
        'tenant_id': fields.many2one('rdm.tenant','Tenant')
    }
    
    _defaults = {
        'tenant_id': lambda self, cr, uid, context: context.get('tenant_id', False),                 
    }
    
rdm_customer()