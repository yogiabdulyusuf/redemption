from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),    
    ('open','Open'),    
    ('done', 'Closed'),
    ('reqdel', 'Request Delete'),
    ('delete', 'Deleted'),
]

AVAILABLE_ADJUST_TYPE = [
    ('+','Add'),    
    ('-','Deduct'),    
]


class rdm_point_adj(osv.osv):
    _name="rdm.point.adj"
    _description =  "Redemption Point Adjustment"
        
    def trans_close(self, cr, uid, ids, context=None):    
        _logger.info("Close Transaction for ID : " + str(ids[0]))    
        self.write(cr,uid,ids,{'state':'done'},context=context)
        self._adjust_point_(cr, uid, ids, context)      
        return True
    
    def print_reciept(self, cr, uid, ids, context=None):
        _logger.info("Print Reciept for ID : " + str(ids[0]))
        
    
    def re_print(self, cr, uid, ids, context=None):
        _logger.info("RePrint Reciept for ID : " + str(ids[0]))
    
    def trans_reset(self, cr, uid, ids, context=None):
        _logger.info("Reset Transaction for ID : " + str(ids[0]))
        self.write(cr,uid,ids,{'state':'open'},context=context)
        return True
    
    def trans_req_delete(self, cr, uid, ids, context=None):
        _logger.info("Delete Request for ID : " + str(ids[0]))
        self.write(cr,uid,ids,{'state':'req_delete'},context=context)         
        return True
    
    def trans_delete(self, cr, uid, ids, context=None):
        _logger.info("Delete Transaction for ID : " + str(ids[0]))
        self.write(cr,uid,ids,{'state':'delete'},context=context) 
        return True
    
    def _get_trans(self, cr, uid, trans_id , context=None):
        return self.browse(cr, uid, trans_id, context=context);
    
    def _adjust_point_(self, cr, uid, ids, context=None):        
        _logger.info('Start Point Adjustment')
        trans_id = ids[0]
        trans = self._get_trans(cr, uid, trans_id, context)                
        point_data = {}
        point_data.update({'customer_id': trans.customer_id.id})
        point_data.update({'adj_id':trans.id})
        point_data.update({'trans_type':'adjust'})
        if trans.adjust_type == '+':
            point_data.update({'point':trans.point})
            point_data.update({'expired_date': trans.expired_date})
            self.pool.get('rdm.customer.point').create(cr, uid, point_data, context=context)
        if trans.adjust_type == '-':        
            customer = self.pool.get('rdm.customer').get_trans(cr, uid, trans.customer_id.id, context=context)
            if customer.point >= trans.point:                                            
                self.pool.get('rdm.customer.point').deduct_point(cr, uid, trans_id, trans.customer_id.id, trans.point, context=context)                
            else:                
                raise osv.except_osv(('Warning'), ('Point not enough for adjustment!'))
        _logger.info('End Point Adjustment')
                                                     
    _columns = {
        'trans_date': fields.date('Date',readonly=True),                                
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),
        'adjust_type': fields.selection(AVAILABLE_ADJUST_TYPE,'Type',size=16, required=True),                
        'point': fields.integer('Point',required=True),    
        'expired_date': fields.date('Expired Date'),
        'printed': fields.boolean('Printed',readonly=True),        
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),        
    }
    
    _defaults = {
        'trans_date': fields.date.context_today,
        'adjust_type': lambda *a: '+',
        'point': lambda *a: 0,
        'printed': lambda *a: False,
        'state': lambda *a: 'draft',        
    }
    
    def create(self, cr, uid, values, context=None):       
        values.update({'state':'open'})
        if values.get('adjust_type') == '+': 
            if values.get('expired_date'):     
                id =  super(rdm_point_adj, self).create(cr, uid, values, context=context)        
                return id
            else:
                raise osv.except_osv(('Warning'), ('Please define Expired Date!'))
        else:
            id =  super(rdm_point_adj, self).create(cr, uid, values, context=context)
            return id        
                                    
rdm_point_adj()
