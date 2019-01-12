from openerp.osv import fields, osv

class rdm_customer_coupon(osv.osv):
    _name = "rdm.customer.coupon"
    _inherit = "rdm.customer.coupon"
    _columns = {
        'reward_trans_id': fields.many2one('rdm.reward.trans','Reward Transaction ID',readonly=True),        
    }
rdm_customer_coupon()