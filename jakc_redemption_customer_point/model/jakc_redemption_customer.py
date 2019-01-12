from openerp.osv import fields, osv
import logging


_logger = logging.getLogger(__name__)

class rdm_customer(osv.osv):    
    _inherit = "rdm.customer"
    
    def get_points(self, cr, uid, ids, field_name, args, context=None):
        id = ids[0]
        res = {}
            
        total_point = self.pool.get('rdm.customer.point').get_customer_total_point(cr, uid, id, context=context)            
        _logger.info('Total Point : ' + str(total_point))        
        
        if total_point is None:
            total_point = 0
                                    
        res[id] = total_point        
        return res
                            
    _columns = {
        'point': fields.function(get_points, type="integer", string='Points'),
        'customer_point_ids': fields.one2many('rdm.customer.point','customer_id','Points',readonly=True)        
    }
            
rdm_customer()