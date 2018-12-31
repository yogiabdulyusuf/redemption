from openerp.osv import fields, osv
from datetime import datetime
import time
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),
    ('active','Active'),
    ('expired','Expired'),
    ('claimed','Claimed'),    
    ('req_delete','Request For Delete'),
    ('delete','Deleted')
]


AVAILABLE_TRANS_TYPE = [
    ('promo','Promotion'),
    ('point','Point'),
    ('reward','Reward'),
    ('reference','Reference'),
    ('member','New Member'),
]


class rdm_customer_coupon(osv.osv):
    _name = 'rdm.customer.coupon'
    _description = 'Redemption Customer Coupon'
                
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def process_expired(self, cr, uid, context=None):
        _logger.info('Start Customer Coupon Process Expired')        
        _logger.info('End Customer Coupon Process Expired')
        return True    
    
    
    
    def delete_coupon(self, cr, uid, ids, context=None):
        _logger.info('Start Delete Coupon')
        trans = self.get_trans(cr, uid, ids, context)        
        customer_coupon_detail_ids = trans.customer_coupon_detail_ids
        for customer_coupon_detail_id in customer_coupon_detail_ids:
            self.pool.get('rdm.customer.coupon.detail').trans_delete(cr, uid, [customer_coupon_detail_id.id], context=context)
        _logger.info('End Delete Coupon')
        
    def undelete_coupon(self, cr, uid, ids, context=None):
        _logger.info('Start UnDelete Coupon')
        trans = self.get_trans(cr, uid, ids, context)        
        customer_coupon_detail_ids = trans.customer_coupon_detail_ids
        for customer_coupon_detail_id in customer_coupon_detail_ids:
            self.pool.get('rdm.customer.coupon.detail').trans_close(cr, uid, [customer_coupon_detail_id.id], context=context)    
        _logger.info('End UnDelete Coupon')
            
    def generate_coupon(self, cr, uid, ids, context=None):
        _logger.info('Start Generate Coupon') 
        trans = self.get_trans(cr, uid, ids, context)
        coupon = trans.coupon
        for i in range (0,coupon):
            values = {}
            values.update({'customer_coupon_id': trans.id})
            values.update({'expired_date':trans.expired_date})        
            self.pool.get('rdm.customer.coupon.detail').create(cr, uid, values, context=context)                    
	    time.sleep(0.1)
        _logger.info('End Generate Coupon')
            
    _columns = {
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),             
        'trans_type': fields.selection(AVAILABLE_TRANS_TYPE, 'Transaction Type', size=16),        
        'coupon': fields.integer('Coupon #', required=True),        
        'expired_date': fields.date('Expired Date', required=True),
        'customer_coupon_detail_ids': fields.one2many('rdm.customer.coupon.detail','customer_coupon_id','Coupon Codes'),
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),
    }        
    
    def create(self, cr, uid, values, context=None):
        id = super(rdm_customer_coupon, self).create(cr, uid, values, context=context)
        self.generate_coupon(cr, uid, [id], context=context)
        return id
    
    _defaults = {
        'coupon': lambda *a: 0,
        'state': lambda *a: 'active',
    }
    
rdm_customer_coupon()

class rdm_customer_coupon_detail(osv.osv):
    _name = 'rdm.customer.coupon.detail'
    _description = 'Redemption Customer Coupon Detail'
        
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids , context=context):
            res.append((record.id, record.coupon_code))
        return res
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, [('coupon_code', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        
        return self.name_get(cr, uid, ids, context=context)
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)    
    
    def trans_delete(self, cr, uid, ids, context=None):
        _logger.info('Start Trans Delete')
        values = {}
        values.update({'state':'delete'})
        self.write(cr, uid, ids, values, context=context)
        _logger.info('End Trans Delete')
    
    def trans_close(self, cr, uid, ids, context=None):
        _logger.info('Start Trans Close')
        values = {}
        values.update({'state':'done'})
        self.write(cr, uid, ids, values, context=context)
        _logger.info('End Trans Close')
    
    def trans_expired(self, cr, uid, ids, context=None):
        _logger.info('Start Trans Expired')
        values = {}
        values.update({'state':'expired'})
        self.write(cr, uid, ids, values, context=context)
        _logger.info('End Trans Expired')
        
    def trans_claimed(self, cr, uid, ids, context=None):
        _logger.info('Start Customer Coupon Detail Process Claimed')       
        values = {}
        values.update({'state':'claimed'})
        super(rdm_customer_coupon_detail,self).write(cr, uid, ids, values, context=context)
        _logger.info('End Customer Coupon Detail Process Claimed')      
        return True  
    
    def trans_re_open(self, cr, uid, ids, context=None):
        _logger.info('Start Customer Coupon Detail Process Re-open')       
        values = {}
        values.update({'state':'active'})
        super(rdm_customer_coupon_detail,self).write(cr, uid, ids, values, context=context)
        _logger.info('End Customer Coupon Detail Process Re-open')      
        return True
    
    def expired_coupon(self, cr, uid, customer_coupon_id, context=None):
        _logger.info('Start Expired Coupon')
        args = {('customer_coupon_id','=',customer_coupon_id)}
        ids = self.search(cr, uid, args, context=context)
        values = {}
        values.update({'state':'expired'})
        self.write(cr, uid, ids, values, context=context)
        _logger.info('End Expired Coupon')
        
    _columns = {
        'customer_coupon_id': fields.many2one('rdm.customer.coupon','Customer Coupon', readonly=True),
        'coupon_code': fields.char('Coupon Code', size=10, required=True, readonly=True),
        'expired_date': fields.date('Expired Date', required=True, readonly=True),
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),
    }
    
    _defaults = {    
        'state': lambda *a: 'active',
    }    

    def create(self, cr, uid, values, context=None):
        coupon_code = self.pool.get('ir.sequence').get(cr, uid, 'rdm.customer.coupon.sequence')
        values.update({'coupon_code': coupon_code})        
        id =  super(rdm_customer_coupon_detail,self).create(cr, uid, values, context=context)
        _logger.info("Generate Coupon : " + coupon_code)        
        return id
                
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        if 'state' in values.keys():
            if values.get('state') == 'claimed':
                return self.process_claimed(cr, uid, ids, context=context)
                
        return super(rdm_customer_coupon_detail, self).write(cr, uid, ids, values, context=context)
    
rdm_customer_coupon_detail()
