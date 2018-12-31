from openerp.osv import fields, osv
from datetime import datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),
    ('open','Open'),    
    ('done', 'Closed'),
    ('expired','Expired'),
    ('deleted','Deleted'),
]

AVAILABLE_TYPE = [
    ('goods','Goods'),
    ('coupon','Coupon'),
]

AVAILABLE_VOUCHER_STATES = [
    ('open','Open'),
    ('done','Closed'),
    ('disable','Disable'),
]

reportserver = '172.16.0.3'
reportserverport = '8080'

class rdm_reward(osv.osv):
    _name = "rdm.reward"
    _description = "Redemption Reward"
    

    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]        
        return self.browse(cr, uid, trans_id, context=context)

    def trans_close(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'done'})
        return super(rdm_reward, self).write(cr, uid, ids, values, context=context)
    
    def trans_re_open(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state':'draft'})
        return super(rdm_reward, self).write(cr, uid, ids, values, context=context)
                
    def get_stocks(self, cr, uid, ids, field_name, args, context=None):
        _logger.info('Start Get Stocks')               
        id = ids[0]     
        trans = self.get_trans(cr, uid, ids, context)
        total = 0
        res = {}
        if trans.type == 'goods':
            total_stock = self.pool.get('rdm.reward.goods').get_stock(cr, uid, id, context=context)
            total_booking = self.pool.get('rdm.reward.trans').get_reward_booking(cr, uid, id, context=context)
            total_usage = self.pool.get('rdm.reward.trans').get_reward_usage(cr, uid, id, context=context)
        if trans.type == 'coupon':
            total_stock = self.pool.get('rdm.reward.coupon').get_stock(cr, uid, id, context=context)
            total_booking = self.pool.get('rdm.reward.trans').get_reward_booking(cr, uid, id, context=context)
            total_usage = self.pool.get('rdm.reward.trans').get_reward_usage(cr, uid, id, context=context)
        res[id] = total_stock - total_booking - total_usage
        _logger.info('End Get Stocks')    
        return res    
        
    def get_bookings(self, cr, uid, ids, field_name, args, context=None):
        _logger.info('Start Get Booking')       
        id = ids[0]
        total = self.pool.get('rdm.reward.trans').get_reward_booking(cr, uid, id, context=context)        
        res = {}
        res[id] = total
        _logger.info('End Get Booking')
        return res       
         
    def get_usages(self, cr, uid, ids, field_name, args, context=None):
        _logger.info('Start Get Usage')        
        id = ids[0]
        total = self.pool.get('rdm.reward.trans').get_reward_usage(cr, uid, id, context=context)        
        res = {}
        res[id] = total
        _logger.info('End Get Usages')                
        return res                         
    
    def trans_reward_expired(self, cr, uid, ids, context=None):
        _logger.info('Start Trans Reward Expired')
        today = datetime.now()
        trans = self.get_trans(cr, uid, ids, context)
        if trans.is_booking:
            if datetime.strptime(trans.booking_expired,'%Y-%m-%d') <= today:         
                values = {}
                values.update({'state':'expired'})
                self.write(cr, uid, ids, values, context=context)
        _logger.info('End Trans Reward Expired')
        return True
        
    def process_reward_expired(self, cr, uid, context=None):
        _logger.info('Start Process Reward Expired')
        today = datetime.now()
        args = [('is_booking','=',True),('booking_expired','<=', today.strftime('%Y-%m-%d'),('state','=','open'))]
        reward_trans_ids = self.search(cr, uid, args, context=context)
        values = {}
        values.update({'state':'expired'})
        self.write(cr, uid, reward_trans_ids, values, context=context)
        _logger.info('End Process Reward Expired')
        return True
                    
    _columns = {
        'name': fields.char('Name', size=100, required=True),
        'type': fields.selection(AVAILABLE_TYPE,'Type', size=16, required=True),
        'iface_instant': fields.boolean('Is Instant'),
        'point': fields.integer('Point #'),
        'coupon_number': fields.integer('Coupon #'),
        'limit_count': fields.integer('Limit Count Per User',required=True),
        'stock': fields.function(get_stocks, type="integer", string="Stock"),
        'booking': fields.function(get_bookings, type="integer", string="Booking"),
        'usage': fields.function(get_usages, type="integer", string="Usage"),                        
        'image1': fields.binary('Image'),
        'reward_trans_ids': fields.one2many('rdm.reward.trans', 'reward_id', 'Transaction'),
        'goods_ids': fields.one2many('rdm.reward.goods', 'reward_id', 'Goods'),
        'coupon_ids': fields.one2many('rdm.reward.coupon', 'reward_id', 'Coupon'),
        'voucher_ids': fields.one2many('rdm.reward.voucher', 'reward_id', 'Voucher'),             
        'state': fields.selection(AVAILABLE_STATES,'Status',size=16,readonly=True),        
    }
    
    _defaults ={
        'point': lambda *a: 1,        
        'type': lambda *a: 'goods',
        'iface_instant': lambda *a: False,
        'limit_count': lambda *a: -1,
        'state': lambda *a: 'draft',
    }

        
rdm_reward()

class rdm_reward_goods(osv.osv):
    _name = "rdm.reward.goods"
    _description = "Redemption Reward Goods"
    
    def get_stock(self, cr, uid, reward_id, context=None):
        _logger.info('Start Get Goods Stocks')        
        total_stock = 0        
        sql_req= "SELECT sum(stock) as total FROM rdm_reward_goods WHERE reward_id=" + str(reward_id) + " AND state='open'"      
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res is not None:
        	if sql_res['total'] is not None:
        		total_stock = sql_res['total']
        	else:
          		total_stock = 0            
        _logger.info('End Get Goods Stocks')        
        return total_stock        
                                
    _columns = {
        'reward_id': fields.many2one('rdm.reward','Reward', readonly=True),
        'trans_date': fields.date('Transaction Date'),     
        'stock': fields.integer('Stock'),
        'state': fields.selection(AVAILABLE_STATES,'Status', size=16, readonly=True)       
    }    

    _defaults = {
        'trans_date': fields.date.context_today,
        'state': 'open',
    }
    
rdm_reward_goods()

class rdm_reward_coupon(osv.osv):
    _name = "rdm.reward.coupon"
    _description = "Redemption Reward Coupon"
    
    def get_stock(self, cr, uid, reward_id, context=None):
        _logger.info('Start Get Coupon Stocks')        
        total_stock = 0        
        sql_req= "SELECT sum(stock) as total FROM rdm_reward_coupon WHERE reward_id=" + str(reward_id)            
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res:
            total_stock = sql_res['total']            
        _logger.info('End Get Coupon Stocks')        
        return total_stock    
        
    _columns = {
        'reward_id': fields.many2one('rdm.reward','Reward', readonly=True),
        'trans_date': fields.date('Transaction Date'),     
        'stock': fields.integer('Stock'),       
    }
    
    _defaults = {
        'trans_date': fields.date.context_today,
    }    
    
rdm_reward_coupon()

class rdm_reward_voucher(osv.osv):
    _name = "rdm.reward.voucher"
    _description = "Redemption Reward Voucher"
    
    def get_stock(self, cr, uid, reward_id, context=None):        
        _logger.info('Start Get Voucher Stocks')        
        total_stock = 0        
        sql_req= "SELECT count(*) as total FROM rdm_reward_voucher WHERE reward_id=" + str(reward_id) + " AND state='open'"            
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res:
            total_stock = sql_res['total']            
        _logger.info('End Get Voucher Stocks')        
        return total_stock    
    
    
    _columns = {
        'reward_id': fields.many2one('rdm.reward','Reward', readonly=True),
        'trans_date': fields.date('Transaction Date'),
        'voucher_no': fields.char('Voucher #', size=15),
        'state': fields.selection(AVAILABLE_VOUCHER_STATES,'Status',size=16, readonly=True),
    }
    
    _defaults = {
        'trans_date': fields.date.context_today,
        'state': lambda *a : 'open',
    }
    
rdm_reward_voucher()

class rdm_reward_trans(osv.osv):
    _name = "rdm.reward.trans"
    _description = "Redemption Reward Transaction"
    
    def trans_reward_expired(self, cr, uid, ids, context=None):
        _logger.info('Start Reward Expired')
        id = ids[0]
        trans = self.get_trans(cr, uid, id, context)
        booking_expired_date = datetime.strptime(trans.booking_expired,'%Y-%m-%d')
        if trans.is_booking == True and booking_expired_date <= datetime.now():
            values = {}
            values.update({'state':'expired'})            
            self.write(cr, uid, ids, values, context=context)
            _logger.info('End Reward Expired')
            return True                
        else:
            raise osv.except_osv(('Warning'), ('Transaction still active'))         
          
        
    def check_reward_limit_count(self, cr, uid, customer_id, reward_id, context=None):
        reward = self.pool.get('rdm.reward').get_trans(cr, uid, [reward_id], context=context)
        if reward.limit_count  == -1:
            return True
        else:
            #sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.reward_id=" + str(reward_id) + " AND c.trans_date='" + datetime.today().strftime('%Y-%m-%d') + "' AND c.state='done'"
            sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.reward_id=" + str(reward_id) + " AND c.state='done'"
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()
            if sql_res:
                total = sql_res['total']
                if total >= reward.limit_count:
                    return False
                else:
                    return True
            else:
                return False
                     
    def check_reward_stock(self, cr, uid, reward_id, context=None):
        reward = self.pool.get('rdm.reward').get_trans(cr, uid, reward_id, context=context) 
        if reward.stock > 0:
            return True
        else:
            return False        
                                   
    def allow_redeem_reward(self, cr, uid, customer_id, reward_id, context=None):        
        reward_config = self._reward_config(cr, uid, context)  
        if reward_config.reward_limit_count  == -1:
            return True
        else:        
            limit_total = reward_config.reward_limit_count
                            
            if reward_config.reward_limit:
                sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.trans_date='" + datetime.today().strftime('%Y-%m-%d') + "' AND c.state='done'"
                cr.execute(sql_req)
                sql_res = cr.dictfetchone()
                if sql_res:
                    current_total = sql_res['total']
                else:
                    current_total = 0                    
                _logger.info('Total Reward Trans : ' + str(current_total) )                    
                
                if current_total >= limit_total:
                    return False
                else:
                    return True
            
            if reward_config.reward_limit_product:
                sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.reward_id=" + str(reward_id) + " AND c.trans_date='" + datetime.today().strftime('%Y-%m-%d') + "' AND c.state='done'"
                cr.execute(sql_req)
                sql_res = cr.dictfetchone()
                if sql_res:
                    current_total = sql_res['total']
                else:
                    current_total = 0
                _logger.info('Total Reward Trans For Product : ' + str(current_total) )                
                
                if current_total >= limit_total:
                    return False
                else:
                    return True
                       
        
                                                                                
    def _reward_config(self, cr, uid, context=None):
        return self.pool.get('rdm.reward.config').get_config(cr, uid, context=context)
    
    def trans_close(self, cr, uid, ids, context=None):    
        _logger.info("Close Transaction for ID : " + str(ids))
        #Close Transaction         
        self.write(cr,uid,ids,{'state':'done'},context=context)        
        self._send_notification_to_customer(cr, uid, ids, context)
        return True
        
    def _update_print_status(self, cr, uid, ids, context=None):
        _logger.info("Start Update Print Status for ID : " + str(ids))
        values = {}
        values.update({'bypass':True})
        values.update({'method':'_update_print_status'})
        values.update({'printed':True})
        self.write(cr, uid, ids, values, context=context)
        _logger.info("End Update Print Status for ID : " + str(ids))            
        
    def trans_print_receipt(self, cr, uid, ids, context=None):
        _logger.info("Print Receipt for ID : " + str(ids))        
        trans_id = ids[0]   
        
        serverUrl = 'http://' + reportserver + ':' + reportserverport +'/jasperserver'
        j_username = 'rdm_operator'
        j_password = 'rdm123'
        ParentFolderUri = '/rdm'
        reportUnit = '/rdm/trans_receipt'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(trans_id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new' 
        }        
            
    def trans_re_print(self, cr, uid, ids, context=None):
        _logger.info("Re-Print Receipt for ID : " + str(ids))
        trans_id = ids[0]
        trans = self._get_trans(cr, uid, trans_id, context)        
        return True
    
    def trans_reset(self, cr, uid, ids, context=None):
        _logger.info("Start Reset for ID : " + str(ids))
        values = {}
        values.update({'bypass':True})
        values.update({'method':'trans_reset'})
        values.update({'state':'open'})
        self.write(cr, uid, ids, values, context=context)
        _logger.info("End Reset for ID : " + str(ids))            

    def onchange_reward_id(self, cr, uid, ids, reward_id, context=None):
        res = {}
        if reward_id:
            reward = self.pool.get('rdm.reward').browse(cr, uid, reward_id, context=context)
            res['point'] = reward.point            
        return {'value':res}
    
    def onchange_is_booking(self, cr, uid, ids, is_booking, context=None):
        res = {}        
        if is_booking == True:         
            rdm_reward_config = self.pool.get('rdm.reward.config').get_config(cr, uid, context=context)            
            expired_date = datetime.today() + timedelta(days=rdm_reward_config.reward_booking_expired_day)   
            res['booking_expired'] = expired_date.strftime('%Y-%m-%d')
        else:
            res['booking_expired'] = None            
        return {'value':res}
      
    def get_trans(self, cr, uid, trans_id , context=None):
        return self.browse(cr, uid, trans_id, context=context);
    
    def _get_reward(self, cr, uid, reward_id, context=None):
        reward = self.pool.get('rdm.reward').browse(cr, uid, reward_id, context=context)
        return reward        
    
    def get_reward_usage(self, cr, uid, reward_id, context=None):
        _logger.info('Start Get Reward Usage')        
        total = 0        
        sql_req= "SELECT count(*) as total FROM rdm_reward_trans WHERE reward_id=" + str(reward_id) + " AND state='done'"      
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res is not None:
            if sql_res['total'] is not None:
                total = sql_res['total']
            else:
                total_ = 0            
        _logger.info('End Get Reward Usage')        
        return total    
    
    def get_reward_booking(self, cr, uid, reward_id, context=None):
        _logger.info('Start Get Reward Booking')        
        total = 0        
        sql_req= "SELECT count(*) as total FROM rdm_reward_trans WHERE is_booking=TRUE AND reward_id=" + str(reward_id) + " AND state='open'"      
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res is not None:
            if sql_res['total'] is not None:
                total = sql_res['total']
            else:
                total_ = 0            
        _logger.info('End Get Reward Booking')        
        return total    
    
    def process_reward_expired(self, cr, uid, context=None):
        _logger.info('Start Process Reward Expired')
        today = datetime.now()
        args = [('is_booking','=',True),('booking_expired','<=', today.strftime('%Y-%m-%d'),('state','=','open'))]
        reward_trans_ids = self.search(cr, uid, args, context=context)
        values = {}
        values.update({'state':'expired'})
        self.write(cr, uid, reward_trans_ids, values, context=context)
        _logger.info('End Process Reward Expired')
        return True
    
    def _send_notification_to_customer(self, cr, uid, ids, context=None):
        _logger.info("Start Notification Process")
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)
        customer_id = trans.customer_id
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        rdm_reward_config = self.pool.get('rdm.reward.config').get_config(cr, uid, context=context)
        if rdm_config.enable_email and customer_id.receive_email:
            #Send Email            
            _logger.info('Send Reward Transaction Notification')
            email_obj = self.pool.get('email.template')        
            template_ids = rdm_reward_config.reward_trans_email_tmpl
            email = email_obj.browse(cr, uid, template_ids)  
            email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
            email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)           
        return True
     
    def _send_booking_notitication_to_customer(self, cr, uid, ids, context=None):
        _logger.info("Start Booking Notification Process")
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)
        customer_id = trans.customer_id
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        rdm_reward_config = self.pool.get('rdm.reward.config').get_config(cr, uid, context=context)
        if rdm_config.enable_email and customer_id.receive_email:
            #Send Email            
            _logger.info('Send Reward Booking Notification')
            email_obj = self.pool.get('email.template')        
            template_ids = rdm_reward_config.reward_booking_email_tmpl
            email = email_obj.browse(cr, uid, template_ids)  
            email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
            email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)
        _logger.info("End Booking Notification Process")           
        return True 

    def _generate_coupon(self, cr, uid, trans_id, context=None):
        _logger.info('Start Generate Coupon')
        trans = self.get_trans(cr, uid, trans_id, context)
        _logger.info('Reward Total Coupon :' + str(trans.reward_id.coupon_number))
        coupon_data = {}
        coupon_data.update({'customer_id':trans.customer_id.id})
        coupon_data.update({'reward_trans_id':trans.id})
        coupon_data.update({'trans_type':'reward'})
        coupon_data.update({'coupon':trans.reward_id.coupon_number})
        coupon_data.update({'expired_date': datetime.now()})
        self.pool.get('rdm.customer.coupon').create(cr, uid, coupon_data, context=context)
        _logger.info('End Generate Coupon')

    def trans_print(self, cr, uid, ids, context=None):
        _logger.info("Print Receipt for ID : " + str(ids))
        self._update_print_status(cr, uid, ids, context)
        id = ids[0]
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        serverUrl = 'http://' + rdm_config.report_server + ':' + rdm_config.report_server_port +'/jasperserver'
        j_username = 'rdm_operator'
        j_password = 'rdm123'
        ParentFolderUri = '/rdm'
        reportUnit = '/rdm/reward_receipt'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new'
        }

    _columns = {
        'trans_date': fields.date('Transaction Date', required=True, readonly=True),        
        'customer_id': fields.many2one('rdm.customer','Customer', required=True),        
        'reward_id': fields.many2one('rdm.reward','Reward', required=True),
        'point': fields.integer('Point # Deduct', readonly=True),
        'customer_coupon_ids': fields.one2many('rdm.customer.coupon','reward_trans_id','Coupons'),
        'remarks': fields.text('Remarks'),
        'is_booking': fields.boolean('Is Booking ?'),
        'booking_expired': fields.date('Booking Expired'),        
        'printed': fields.boolean('Printed', readonly=True),        
        're_print': fields.integer('Re-Print'),
        're_print_remarks': fields.text('Re-print Remarks'),        
        'state':  fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),        
    }
    
    _defaults = {                
        'trans_date': fields.date.context_today,
        'state': lambda *a: 'draft',
        'is_booking': lambda *a: False,        
        'printed': lambda *a: False,    
    }
    
    def create(self, cr, uid, values, context=None):                        
        customer_id = values.get('customer_id')
        reward_id = values.get('reward_id')         
                       
        reward_stock = self.check_reward_stock(cr, uid, [reward_id] , context=context)      
        _logger.info("Reward Stock : " + str(reward_stock))  
        if not reward_stock:
            raise osv.except_osv(('Warning'), ('Reward has no stock'))
        
        check_reward_limit_count  = self.check_reward_limit_count(cr, uid, customer_id, reward_id, context)
        if not check_reward_limit_count:
            raise osv.except_osv(('Warning'), ('Reward Limit Count Applied'))
                    
        allow_redeem_reward = self.allow_redeem_reward(cr, uid, customer_id, reward_id, context=context)        
        if not allow_redeem_reward:
            raise osv.except_osv(('Warning'), ('Redeem Limit Applied'))
            
        customer_id = self.pool.get('rdm.customer').get_trans(cr, uid, customer_id, context=context)            
        reward = self._get_reward(cr, uid, reward_id, context)        
        if customer_id.point < reward.point:
            raise osv.except_osv(('Warning'), ('Point not enough'))            
        
        values.update({'point':reward.point})
        values.update({'state':'open'})            
        trans_id = super(rdm_reward_trans,self).create(cr, uid, values, context=context)
        if values.get('is_booking') == True:
            self.pool.get('rdm.customer.point').deduct_point(cr, uid, trans_id, customer_id.id, values.get('point'), context=context)
            self._send_booking_notitication_to_customer(cr, uid, [trans_id], context)
        return trans_id
        
    def write(self, cr, uid, ids, values, context=None ):
        trans_id = ids[0]                
        trans = self.get_trans(cr, uid, trans_id, context)
                    
        if trans['state'] == 'done':
            #Modify Closed Transaction             
            if values.get('bypass') == True:
                trans_data = {}
                if values.get('method') == 'trans_reset':
                    trans_data.update({'state': values.get('state')})
                if values.get('method') == 'trans_print_receipt':
                    trans_data.update({'printed': values.get('printed')})                
                result = super(rdm_reward_trans,self).write(cr, uid, ids, trans_data, context=context)                       
            else: 
                raise osv.except_osv(('Warning'), ('Edit not allowed, Transaction already closed!'))              
        else:
            #Close Transaction
            if values.get('state') == 'done':
                #Check Stock                
                if not trans.is_booking:                    
                    reward_id = trans.reward_id.id
                    reward_stock = self.check_reward_stock(cr, uid, [reward_id], context)
                    if not reward_stock:
                        raise osv.except_osv(('Warning'), ('Reward has no stock'))
                     
                #Close Transaction
                trans = self.get_trans(cr, uid, trans_id, context)                                        
                result = super(rdm_reward_trans,self).write(cr, uid, ids, values, context=context)
                
                #Deduct Point
                customer_id = trans.customer_id.id
                
                #Deduct point if not booking transaction                
                if not trans.is_booking:
                    self.pool.get('rdm.customer.point').deduct_point(cr, uid, trans_id, customer_id, trans.point, context=context)
                    if trans.reward_id.type == 'coupon':
                        _logger.info("Generate Coupon " + str(trans.reward_id.coupon_number))
                        self._generate_coupon(cr, uid, trans_id, context=context)

            #Expired Booking Transaction                                
            elif values.get('state') == 'expired':
                result = super(rdm_reward_trans,self).write(cr, uid, ids, values, context=context)
            #Other State
            else:            
                trans = self.get_trans(cr, uid, trans_id, context)
                if 'customer_id' in values.keys():
                    customer_id = values.get('customer_id')
                else:
                    customer_id = trans.customer_id.id
                if 'reward_id' in values.keys():                    
                    reward_id = values.get('reward_id')
                else:
                    reward_id = trans.reward_id.id
                    
                allow_redeem_reward = self.allow_redeem_reward(cr, uid, customer_id, reward_id, context=context)    
                if allow_redeem_reward:
                    customer = self.pool.get('rdm.customer').get_trans(cr, uid, customer_id, context=context)            
                    reward = self._get_reward(cr, uid, reward_id, context)            
                    if customer['point'] >= reward.point:            
                        values.update({'point':reward.point})
                        values.update({'state':'open'})            
                        result = super(rdm_reward_trans,self).write(cr, uid, [trans.id], values, context=context)                                
                    else:
                        raise osv.except_osv(('Warning'), ('Point not enough'))           
                else:
                    raise osv.except_osv(('Warning'), ('Redeem Limit Applied'))                                                        
        return result
    
rdm_reward_trans()