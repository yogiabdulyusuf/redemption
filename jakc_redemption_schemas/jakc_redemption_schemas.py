
from openerp.osv import fields, osv
from datetime import datetime
import logging
from decimal import Context

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','Draft'),
    ('waiting','Waiting'),
    ('review','Review'),
    ('open','Open'),    
    ('pause','Pause'),                    
    ('done','Close'),    
]

AVAILABLE_BLAST_STATES = [
    ('draft','Draft'),
    ('ready','Ready'),
    ('process','Process'),                        
    ('done','Close'),    
    ('failed','Failed'),
]

AVAILABLE_EMAIL_STATES = [
    ('draft','Draft'),
    ('ready','Ready'),
    ('sent','Sent'),                        
    ('failed','Failed'),
]

AVAILABLE_TYPE_STATES = [
    ('email','Email'),
    ('sms','SMS'),
]

AVAILABLE_CALCULATION = [
    ('ditotal','Ditotal'),
    ('terbesar','Terbesar'),                         
]

AVAILABLE_SEARCH_TYPE_STATES = [
    ('all','All'),
    ('customer','Customer'),
    ('gender','Gender'),
    ('ethnic','Ethnic'),
    ('religion','Religion'),
    ('marital','Marital'),
    ('interest','Interest'),
    ('occupation','Occupation'),
    ('zone','Zone'),    
]


class rdm_schemas_segment(osv.osv):
    _name = 'rdm.schemas.segment'
    _description = 'Redemption Trans Segment'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','Schemas', readonly=True),
        'age_segment': fields.many2one('rdm.age.segment','Age Segment'),
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_segment()   

class rdm_schemas_gender(osv.osv):
    _name = 'rdm.schemas.gender'
    _description = 'Redemption Schemas gender'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','Schemas', readonly=True),
        'gender_id': fields.many2one('rdm.customer.gender','Gender'),        
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}        
rdm_schemas_gender()


class rdm_schemas_ayc_participant(osv.osv):
    _name = 'rdm.schemas.ayc.participant'
    _description = 'Redemption Trans AYC Participant'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','Schemas', readonly=True),
        'participant_id': fields.selection([('1','AYC non participant tenant'),('2','AYC participant tenant')],'Participant Type',required=True),
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_ayc_participant()   


class rdm_schemas_religion(osv.osv):
    _name = 'rdm.schemas.religion'
    _description = 'Redemption Schemas Religion'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','Schemas', readonly=True),
        'religion_id': fields.many2one('rdm.customer.religion','Religion'),        
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_religion()

class rdm_schemas_ethnic(osv.osv):
    _name = 'rdm.schemas.ethnic'
    _description = 'Redemption Schemas Ethnic'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','Schemas', readonly=True),
        'ethnic_id': fields.many2one('rdm.customer.ethnic','Ethnic'),
    }   
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_ethnic()   

class rdm_schemas_tenant(osv.osv):
    _name = 'rdm.schemas.tenant'
    _description = 'Redemption schemas Tenant'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'tenant_id': fields.many2one('rdm.tenant','Tenant'),
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_tenant()   

class rdm_schemas_marital(osv.osv):
    _name = 'rdm.schemas.marital'
    _description = 'Redemption schemas Marital'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'marital_id': fields.many2one('rdm.customer.marital','Marital'),
    }   
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_marital()   

class rdm_schemas_interest(osv.osv):
    _name = 'rdm.schemas.interest'
    _description = 'Redemption schemas Interest'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'interest_id': fields.many2one('rdm.customer.interest','Interest'),
    }    
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_interest()   

class rdm_schemas_card_type(osv.osv):
    _name = 'rdm.schemas.card.type'
    _description = 'Redemption schemas Card Type'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'card_type_id': fields.many2one('rdm.card.type','Card Type'),
    }   
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_card_type()   

class rdm_schemas_tenant_category(osv.osv):
    _name = 'rdm.schemas.tenant.category'
    _description = 'Redemption schemas Tenant Category'
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'tenant_category_id': fields.many2one('rdm.tenant.category','Tenant Category'),
    }   
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),}
        
rdm_schemas_tenant_category()   

class rdm_schemas_rules(osv.osv):
    _name = 'rdm.schemas.rules'
    _description = 'Redemption schemas Rules'
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_set_global(self, cr, uid, ids, context=None):
        schema = 'spending'
        trans = self.get_trans(cr, uid, ids, context=context)
        if trans:
            if not trans.is_global:
                rules_id = trans.rules_id            
                rules_detail_ids = rules_id.rules_detail_ids
                status = False
                for rules_detail_id in rules_detail_ids:
                    rule_schema = rules_detail_id.rule_schema
                    if rule_schema  == schema:
                        status = True
                if status:
                    values = {}
                    values.update({'is_global':True})
                    self.write(cr, uid, ids, values, context=context)
                else:
                    raise osv.except_osv(('Warning'), ('Please Provide <b>Spending Rule Schema!</b>'))
            else:
                raise osv.except_osv(('Warning'), ('Already Set Global!'))                
    
    def trans_unset_global(self, cr, uid, ids, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)
        if trans:
            if trans.is_global:
                values = {}
                values.update({'is_global':False})
                self.write(cr, uid, ids, values, context=context)
            else:
                raise osv.except_osv(('Warning'), ('Rules is not Global'))
        
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas','schemas', readonly=True),
        'rules_id': fields.many2one('rdm.rules','Rules'),
        'is_global': fields.boolean('Is Global', readonly=True),
        'schemas': fields.selection([('ditotal','Ditotal'),('terbesar','Terbesar')],'Schemas'),
    }   
    _defaults = {
        'schemas_id': lambda self, cr, uid, context: context.get('schemas_id', False),
        'is_global': lambda *a: False,
    }
    
        
rdm_schemas_rules()   

class rdm_schemas_blast(osv.osv):
    _name = 'rdm.schemas.blast'
    _description = 'Redemption Schemas Blast'
    
    def trans_ready(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'ready'})  
        return True
    
    def trans_process(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'process'})  
        return True

    def trans_done(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'done'})  
        return True
        
    def trans_failed(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'failed'})  
        return True
    
    def _get_trans(self, cr, uid, trans_id, context=None):
        return self.browse(cr, uid, trans_id, context=context)
    
    def blast_customer(self, cr, uid, ids, context=None):
        return {
               'type': 'ir.actions.act_window',
               'name': 'Blast Customer',
               'view_mode': 'form',
               'view_type': 'form',                              
               'res_model': 'rdm.schemas.blast.customer',
               'nodestroy': True,
               'target':'new',
               'context': {'blast_id': ids[0]},
        } 
            
    _columns = {
        'schemas_id': fields.many2one('rdm.schemas', 'Schemas', readonly=True),
        'description': fields.text('Description'),
        'customer_schemas_blast_ids': fields.many2many(
                                         'rdm.customer',
                                         'customer_schemas_blast_rel',
                                         'rdm_customer_id',
                                         'rdm_schemas_blast_id',
                                         string = "Customers"),
        'schedule': fields.datetime('Schedule',required=True),        
        'type': fields.selection(AVAILABLE_TYPE_STATES,'Type', size=16, required=True),
        'blast_detail_ids': fields.one2many('rdm.schemas.blast.detail','blast_id', readonly=True),
        'state': fields.selection(AVAILABLE_BLAST_STATES, 'Status', size=16, readonly=True),
    }
    
    _defaults = {
        'state': lambda *a: 'draft',        
    }
    
rdm_schemas_blast()

    
class rdm_schemas_blast_detail(osv.osv):
    _name = 'rdm.schemas.blast.detail'
    _description = 'Redemption Schemas Blast Detail'
    
    def trans_ready(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'ready'})  
        return True
    
    def trans_sent(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'sent'})  
        return True
     
    def trans_failed(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'failed'})  
        return True
    
    _columns = {
        'blast_id': fields.many2one('rdm.schemas.blast', 'Schemas Blast', readonly=True,  ondelete='cascade'),            
        'customer_id': fields.many2one('rdm.customer', 'Customer', required=True),
        'state': fields.selection(AVAILABLE_EMAIL_STATES, 'Status', size=16, readonly=True)
    }
    
    _defaults = {
        'state': lambda *a: 'draft',
    }
    
rdm_schemas_blast_detail()

class rdm_schemas_blast_customer(osv.osv_memory):
    _name = 'rdm.schemas.blast.customer'
    _description = 'Redemption Schema Blast Customer'
    
    def _check_customer(self, cr, uid, blast_id, customer_id, context=None):
        detail_ids = self.pool.get('rdm.schemas.blast.detail').search(cr, uid, [('blast_id','=', blast_id),('customer_id','=',customer_id)] , context=context)
        if len(detail_ids) > 0:
            return True
        else:
            return False
        
    def add_customer(self, cr, uid, ids, context=None):
        _logger.info('Start Add Customer')
        params = self.browse(cr, uid, ids, context=context)
        param = params[0]           
        blast_id = context.get('blast_id')
        if param.search_type == 'all':
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('state','=','active'),], context=context)
            for i in range(len(customer_ids)):
                if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                    data = {}
                    data.update({'blast_id':blast_id})
                    data.update({'customer_id': customer_ids[i]})                
                    self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)
                    
        if param.search_type == 'customer':
            customer_id = param.customer_id.id
            if not self._check_customer(cr, uid, blast_id, customer_id, context=context):
                data = {}
                data.update({'blast_id':blast_id})
                data.update({'customer_id': customer_id})            
                self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)
                
        if param.search_type == 'gender':            
            gender_id = param.gender_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('gender','=',gender_id),('state','=','active')],context=context)
            if len(customer_ids) > 0:                    
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):                
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})            
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
            
        if param.search_type == 'ethnic':            
            ethnic_id = param.enthic_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('ethnic','=',ethnic_id),('state','=','active')])
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):                
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})            
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
                    
        if param.search_type == 'religion':
            religion_id = param.religion_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('religion','=',religion_id)], context=context)
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)                
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
            
        if param.search_type == 'marital':
            marital_id = param.marital_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('marital','=',marital_id)], context=context)
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)                
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
        
        if param.search_type == 'education':
            education_id = param.education_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('education','=',education_id)], context=context)
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)                
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
        
        if param.search_type == 'interest':
            interest_id = param.interest_id.id            
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('interest_id','=',interest_id)], context=context)
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)                
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
            
        if param.search_type == 'occupation':
            occupation_id = param.occupation_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('occupation','=',occupation_id)], context=context)
            if len(customer_ids) > 0:         
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)                
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
        

        if param.search_type == 'zone':
            zone_id = param.zone_id.id
            customer_ids = self.pool.get('rdm.customer').search(cr, uid, [('zone','=',zone_id)], context=context)
            if len(customer_ids) > 0:                 
                for i in range(len(customer_ids)):
                    if not self._check_customer(cr, uid, blast_id, customer_ids[i], context=context):
                        data = {}
                        data.update({'blast_id':blast_id})
                        data.update({'customer_id': customer_ids[i]})                
                        self.pool.get('rdm.schemas.blast.detail').create(cr, uid, data, context=context)
            else:
                raise osv.except_osv(('Warning'), ('No Customer Found!'))
                                    
        _logger.info('End Add Customer')    
        
        return False
        
    _columns = {
        'search_type': fields.selection(AVAILABLE_SEARCH_TYPE_STATES,'Search Type', size=16, required=True),
        'customer_id': fields.many2one('rdm.customer','Customer'),        
        'gender_id': fields.many2one('rdm.customer.gender','Customer Gender'),
        'ethnic_id': fields.many2one('rdm.customer.ethnic','Customer Ethnic'),
        'religion_id': fields.many2one('rdm.customer.religion','Customer Religion'),
        'marital_id': fields.many2one('rdm.customer.marital','Customer Marital'),        
        'education_id': fields.many2one('rdm.customer.education','Customer Education'),
        'interest_id': fields.many2one('rdm.customer.education','Customer Interest'),
        'occupation_id': fields.many2one('rdm.customer.occupation','Customer Occupation'),        
        'zone_id': fields.many2one('rdm.customer.zone','Customer Zone'),                    
    }
    
class rdm_schemas(osv.osv):
    _name = 'rdm.schemas'
    _description = 'Redemption schemas'
                
    def trans_review(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'review'})
        #Send Email To Manager  
        return True
    
    def trans_start(self, cr, uid, ids, context=None):      
        self.write(cr,uid,ids,{'state':'open'})  
        return True
   
    def trans_pause(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'pause'})  
        return True
    
    def trans_close(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'done'})  
        return True

    def trans_reset(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'open'})  
        return True
    
    def trans_waiting(self, cr, uid, ids, context=None):        
        self.write(cr,uid,ids,{'state':'waiting'})  
        return True
    
    def get_trans(self, cr, uid, ids , context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context);
    
    def active_schemas(self, cr, uid, context=None):
        ids = self.pool.get('rdm.schemas').search(cr, uid, [('state','=','open'),('type','=','promo'),], context=context)
        return self.pool.get('rdm.schemas').browse(cr, uid, ids, context=context)
    
    def promo_to_close(self, cr, uid, context=None):
        today = datetime.now().strftime('%Y-%m-%d')
        args = [('state','=','open'),('end_date','<',today)]
        ids = self.search(cr, uid, args, context=context)
        values = {}
        values.update({'state':'done'})
        self.write(cr, uid, ids, values, context=context)
        return True
                
    def active_promo_schemas(self, cr, uid, context=None):
        ids = {}
        today = datetime.now().strftime('%Y-%m-%d')
        ids = self.pool.get('rdm.schemas').search(cr, uid, [('state','=','open'),('type','=','promo'),('start_date','<=',today),('end_date','>=', today)], context=context)
        return self.pool.get('rdm.schemas').browse(cr, uid, ids, context=context)

    def active_point_schemas(self, cr, uid, context=None):
        ids = {}
        today = datetime.now().strftime('%Y-%m-%d')
        ids = self.pool.get('rdm.schemas').search(cr, uid, [('state','=','open'),('type','=','point'),('start_date','<=',today),('end_date','>=', today)], context=context)
        return self.pool.get('rdm.schemas').browse(cr, uid, ids, context=context)
    
    
    def start_blast(self, cr, uid, context=None):
        _logger.info("Start Schemas Blast")
        active_schemas = self.pool.get('rdm.schemas').active_schemas(cr, uid, context=context)
        for schemas in active_schemas:
            blast_ids = schemas.blast_ids
            for blast in blast_ids:
                if blast.state == 'ready':
                    blast_schedule  = datetime.strptime(blast.schedule, '%Y-%m-%d %H:%M:%S')
                    if blast_schedule <= datetime.now():                        
                        _logger.info('Email Blast for ' + schemas.name + ' executed')
                        self.pool.get('rdm.schemas.blast').trans_process(cr, uid, [blast.id],context=context)
                        email_from = 'info@taman-anggrek-mall.com'
                        subject = schemas.name
                        body_html = schemas.desc_email
                        blast_customer_schemas_blast_ids = blast.customer_schemas_blast_ids
                        #blast_detail_ids = blast.blast_detail_ids
                        for customer_id in blast_customer_schemas_blast_ids:                            
                            if customer_id.receive_email:
                                _logger.info('Send Email to ' + customer_id.name)
                                email_to = customer_id.email
                                message = {}
                                message.update({'email_from':email_from})
                                message.update({'email_to':email_to})
                                message.update({'subject':subject})
                                message.update({'body_html':body_html})
                                self._send_email_notification(cr, uid, message, context)
                            else:
                                _logger.info('Send Email to ' + customer_id.name + ' not allowed!')
                        self.pool.get('rdm.schemas.blast').trans_done(cr, uid, [blast.id],context=context)                        
        _logger.info("End Schemas Blast")
        
    def close_schemas_scheduler(self, cr, uid, context=None):
        _logger.info("Start Close Schemas Scheduler")
        result = self.promo_to_close(cr, uid, context=context)
        return result
        _logger.info("End Close Schemas Scheduler")

    def _get_open_schemas(self, cr, uid, trans_id, context=None):        
        trans = self._get_trans(cr, uid, trans_id, context)     
        ids = None   
        if trans.type == 'promo':
            ids = self.pool.get('rdm.schemas').search(cr, uid, [('type','=','promo'),('state','=','open'),], context=context)
        if trans.type == 'point':
            ids = self.pool.get('rdm.schemas').search(cr, uid, [('type','=','point'),('state','=','open'),], context=context)            
        if ids:
            return True
        else:
            return False        

    def _send_email_notification(self, cr, uid, values, context=None):
        _logger.info('Start Send Email Notification')
        mail_mail = self.pool.get('mail.mail')
        mail_ids = []
        mail_ids.append(mail_mail.create(cr, uid, {
            'email_from': values['email_from'],
            'email_to': values['email_to'],
            'subject': values['subject'],
            'body_html': values['body_html'],
            }, context=context))
        result_id = mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info('Mail ID : ' + str(result_id))
        _logger.info('End Send Email Notification') 
    
    _columns = {
        'name': fields.char('Name', size=200, required=True),
        'type': fields.selection([('promo','Promo'),('point','Point')],'Type',readonly=True),
        'calculation': fields.selection(AVAILABLE_CALCULATION,'Calculation',size=16,required=True),        
        'description': fields.text('Description',required=True),
        'desc_email': fields.text('Description For Email',required=True),
        'desc_sms': fields.char('Description For SMS', size=140,required=True),
        
        #Periode
        'start_date': fields.date('Start Date',required=True),
        'end_date': fields.date('End Date',required=True),
        'last_redeem': fields.date('Last Redeem',required=True),                
        'draw_date': fields.date('Draw Date',required=True),
        
        #Spend, coupon , point and reward
        'max_spend_amount': fields.float('Maximum Spend Amount', required=True, help="-1 for No Limit"),
        'max_spend_amount_global': fields.boolean('Global'),
        'max_coupon': fields.integer('Maximum Coupon'),
        'max_coupon_global': fields.boolean('Maximum Coupon Global'),
        'max_point': fields.integer('Maximum Point'),
        'max_point_global': fields.boolean('Maximum Point Global'),
        'min_spend_amount': fields.float('Minimum Spend Amount', required=True, help="-1 for No Limit"),            
        'coupon_spend_amount': fields.float('Coupon Spend Amount',required=True),
        'point_spend_amount': fields.float('Point Spend Amount',required=True),
        'reward_spend_amount': fields.float('Reward Spend Amount', required=True),
        'limit_coupon': fields.integer('Coupon Limit',help="-1 for No Limit",required=True),
        'limit_coupon_per_periode': fields.integer('Coupon Limit Per Periode', help="-1 for No Limit",required=True),
        'min_coupon': fields.integer('Minimum Coupon'),        
        'limit_point': fields.integer('Point Limit',help="-1 for No Limit",required=True),
        'limit_point_per_periode': fields.integer('Point Limit Per Periode', help="-1 for No Limit", required=True),
        'min_point': fields.integer('Minimum Point'),        
        'limit_reward': fields.integer('Reward Limit',help="-1 for No Limit",required=True),
        'point_expired_date': fields.date('Point Expired Date'),
        
        
        'segment_ids': fields.one2many('rdm.schemas.segment','schemas_id','Segment'),
        'image1': fields.binary("schemas Image"),

        #Bank Promo
        'bank_id': fields.many2one('rdm.bank','Bank Promo'),
                
        #Customer Filter
        'gender_ids': fields.one2many('rdm.schemas.gender','schemas_id','schemas Gender'),
        'religion_ids': fields.one2many('rdm.schemas.religion','schemas_id','schemas Religion'),
        'ethnic_ids': fields.one2many('rdm.schemas.ethnic','schemas_id','schemas Ethnic'),        
        'marital_ids': fields.one2many('rdm.schemas.marital','schemas_id','schemas Marital'),
        'interest_ids': fields.one2many('rdm.schemas.interest','schemas_id','schemas Interest'),
        'card_type_ids': fields.one2many('rdm.schemas.card.type','schemas_id','schemas AYC Card Type'),  
        
        #Tenant Filter
        'tenant_ids': fields.one2many('rdm.schemas.tenant','schemas_id','schemas Tenant'),          
        'tenant_category_ids': fields.one2many('rdm.schemas.tenant.category','schemas_id','Tenant Category'),
        'ayc_participant_ids': fields.one2many('rdm.schemas.ayc.participant','schemas_id','AYC Participant'),            
        
        #Rules List        
        'rules_ids': fields.one2many('rdm.schemas.rules','schemas_id','Rules'),        
        
        #Blast List
        'blast_ids': fields.one2many('rdm.schemas.blast','schemas_id','Blast'),
        
        #Receipt Header and Footer
        'receipt_header': fields.char('Receipt Header', size=50),
        'receipt_footer': fields.text('Receipt Footer'),
        'state':  fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
    }
    _defaults = {        
        'max_spend_amount': lambda *a: -1,
        'reward_spend_amount': lambda *a: -1,
        'state': lambda *a: 'draft',
        'draw_date': fields.date.context_today,
        'limit_coupon': lambda *a: -1,
        'limit_coupon_per_periode': lambda *a: -1,
        'limit_point': lambda *a: -1,
        'limit_reward': lambda *a: -1,
    }
        
    def create(self, cr, uid, values, context=None):
        if 'point_spend_amount' in values.keys():
            if values.get('point_spend_amount') > 0:
                if not values.get('point_expired_date'):
                    raise osv.except_osv(('Warning'), ('Point Expired Date Required!'))
            
        id =  super(rdm_schemas, self).create(cr, uid, values, context=context)
        self.trans_waiting(cr, uid, [id], context)
        return id    

    def write(self, cr, uid, ids, values, context=None):    
        if 'point_spend_amount' in values.keys():
            if values.get('point_spend_amount') > 0:
                if not values.get('point_expired_date'):
                    raise osv.except_osv(('Warning'), ('Point Expired Date Required!'))
            
        result =  super(rdm_schemas, self).write(cr, uid, ids, values, context=context)        
        return result    

rdm_schemas()
