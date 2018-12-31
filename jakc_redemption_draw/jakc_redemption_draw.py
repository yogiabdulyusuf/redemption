from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES=[
    ('draft','New'),
    ('open','Open'),
    ('done','Close'),
]

class rdm_schemas(osv.osv):
    _name = "rdm.schemas"
    _inherit = "rdm.schemas"
    _columns = {
        'draw_ids': fields.one2many('rdm.draw','schemas_id','Draws'),
    }
    
rdm_schemas()
     
class rdm_draw(osv.osv):
    _name = "rdm.draw"
    _description = "Redemption Draw"
        
    _columns = {
        'name': fields.char('Name', size=100, required=True),
        'schemas_id': fields.many2one('rdm.schemas', 'Schemas', required=True),
        'quantity': fields.integer('Quantity', required=True),
        'sequence': fields.integer('Sequence'),
    }
    
    _defaults = {
        'quantity': lambda *a: 1,
    }
    
rdm_draw()

class rdm_draw_detail(osv.osv):
    _name = "rdm.draw.detail"
    _description = "Redemption Draw Detail"
    
    def get_trans(self, cr, uid, ids, context=None):
        return self.browse(cr, uid, ids[0], context=context)

    def trans_confirm(self, cr, uid, ids, context=None):        
        _logger.info('Start Trans Confirm')
        trans = self.get_trans(cr, uid, ids, context=context)
        schemas_id = trans.schemas_id.id
        customer_id = trans.customer_id.id
        is_get = self._check_customer_by_schemas(cr, uid, schemas_id, customer_id, context=context)
        if is_get:
            raise osv.except_osv(('Warning'), ('Customer already get the prize!'))
        customer = self.pool.get('rdm.customer').browse(cr, uid, customer_id, context=context)
        if customer:
            if customer.state != 'active':
                raise osv.except_osv(('Warning'), ('Customer disable or blacklist'))        
                
        values = {}
        values.update({'state': 'done'})        
        super(rdm_draw_detail,self).write(cr, uid, ids, values, context=context)
        coupon_id = trans.coupon_id.id
        _logger.info('Start Detail Trans Claimed')
        self.pool.get('rdm.customer.coupon.detail').trans_claimed(cr, uid, [coupon_id], context=context)
        _logger.info('End Trans Confirm')
            
        return True
        
    def trans_re_open_01(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state': 'open'})
        super(rdm_draw_detail,self).write(cr, uid, ids, values, context=context)
        return True
    
    def trans_re_open_02(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        values = {}
        values.update({'state': 'open'})
        super(rdm_draw_detail,self).write(cr, uid, ids, values, context=context)
        coupon_id = trans.coupon_id.id
        self.pool.get('rdm.customer.coupon.detail').trans_re_open(cr, uid, [coupon_id], context=context)
        return True
                    
    def trans_show_display(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        if trans.state == 'done':
            values = {}
            values.update({'iface_show': True})
            return super(rdm_draw_detail,self).write(cr, uid, ids, values, context=context)
        else:
            raise osv.except_osv(('Warning'), ('Please confirm this transaction first!'))
    
    def trans_close_display(self,cr, uid, ids, context=None):
        values = {}
        values.update({'iface_show': False})
        return super(rdm_draw_detail,self).write(cr, uid, ids, values, context=context)
                
    def onchange_coupon_id(self, cr, uid, ids, coupon_id, context=None):
        res = {}
        if coupon_id:
            coupon_detail = self.pool.get('rdm.customer.coupon.detail').browse(cr, uid, coupon_id, context=context)
            if coupon_detail:
                customer_id = coupon_detail.customer_coupon_id.customer_id
                res['customer_id'] = customer_id.id           
            return {'value':res}        
    
    def _update_customer_id(self, cr, uid, ids, values, context=None):           
        trans = self.get_trans(cr, uid, ids, context=context)        
        customer_id = trans.coupon_id.customer_coupon_id.customer_id
        values.update({'customer_id':customer_id.id})
        return super(rdm_draw_detail, self).write(cr, uid, ids, values, context=context)

    def _check_customer_by_schemas(self, cr, uid, schemas_id, customer_id, context=None):
        args = [('schemas_id','=',schemas_id),('customer_id','=',customer_id),('state','=','done')]
        ids  = self.search(cr, uid, args, context=context)        
        if ids:
            return True
        else:
            return False    
        
        
    _columns = {
        'draw_id': fields.many2one('rdm.draw', 'Draw #', readonly=True),
        'schemas_id': fields.many2one('rdm.schemas','Draw Detail #', readonly=True),
        'coupon_id': fields.many2one('rdm.customer.coupon.detail', 'Coupon #'),
        'customer_id': fields.many2one('rdm.customer', 'Customer', readonly=True),
        'sequence': fields.integer('Sequence', readonly=True),
        'iface_show': fields.boolean('Display', readonly=True), 
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
    }
    
    _defaults = {
        'iface_show': lambda *a: False,
        'state': lambda *a: 'draft'
    }
        
    def write(self,cr, uid, ids, values, context=None):        
        trans = self.get_trans(cr, uid, ids, context=context)                    

        if trans.state == 'done':
            raise osv.except_osv(('Warning'), ('Transaction already closed!'))
                                        
        result = super(rdm_draw_detail, self).write(cr, uid, ids, values, context=context)
        
        if 'coupon_id' in values.keys():                        
            self._update_customer_id(cr, uid, ids, values, context=context)
        
        return result
    
rdm_draw_detail()