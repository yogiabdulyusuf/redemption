from odoo import api, fields, models
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError, Warning
import logging
import re
import logging
import string
import random
import jakc_redemption_customer_config
import uuid

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [
    ('draft','New'),    
    ('active','Active'),    
    ('blacklist','Black List'),    
    ('disable', 'Disable'),
]

CONTACT_TYPES = [
    ('customer','Customer'),
    ('tenant','Tenant'),
    ('both','Customer or Tenant'),    
]


class rdm_customer_change_password(models.Model):
    _name = "rdm.customer.change.password"
    _description = "Redemption Customer Change Password" 
        
    def change_password(self):                
        params = self.browse(cr, uid, ids, context=context)
        param = params[0]           
        customer_id = context.get('customer_id',False)
        data = {}              
        if param.password_new == param.password_confirm:
            data.update({'password':param.password_new})
            self.env('rdm.customer').write(cr, uid, [customer_id], data, context=context)                                                
        return True
    
    _columns = {
        'password_new': fields.char('New Password', size=50),
        'password_confirm': fields.text('Confirm Password', size=50),
    }    
       
rdm_customer_change_password()

class rdm_customer(models.Model):
    _name = 'rdm.customer'
    _description = 'Redemption Customer'
    
    def set_black_list(self, cr, uid, id, context=None):
        _logger.info("Blacklist ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'blacklist'},context=context)
        return True
    
    def set_remove_black_list(self, cr, uid, id, context=None):
        _logger.info("Reset Blacklist ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'active'},context=context)              
        return True
    
    def set_disable(self, cr, uid, id, context=None):
        _logger.info("Activate ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'disable'},context=context)              
        return True
    
    def set_enable(self, cr, uid, id, context=None):
        _logger.info("Reset activate ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'active'},context=context)              
        return True    
        
    def get_trans(self, cr, uid, trans_id , context=None):
        return self.browse(cr, uid, trans_id, context=context);
    
    def change_password(self):
        return {
               'type': 'ir.actions.act_window',
               'name': 'Change Password',
               'view_mode': 'form',
               'view_type': 'form',                              
               'res_model': 'rdm.customer.change.password',
               'nodestroy': True,
               'target':'new',
               'context': {'customer_id': ids[0]},
        } 
    
    def _request_forget_password(self):
        _logger.info('Start Request Forget Password Process')
        values = {}
        values.update({'request_change_password': True})
        values.update({'request_change_password_passcode': str(uuid.uuid1()).replace('-','')})
        result = super(rdm_customer, self).write(cr, uid, ids, values, context=context)
        if result:
            self._send_request_reset_password_notification(cr, uid, ids, context=context)
        _logger.info('End Request Forget Password Process')
        
    def _forget_password(self):
        _logger.info('Start Forget Password Process')
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)    
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)        
        
        if not rdm_config.enable_email:
            raise osv.except_osv(('Warning'), ('Customer cannot Receive Email'))
        
        if not trans.receive_email:
            raise osv.except_osv(('Warning'), ('Customer cannot Receive Email'))                          
        
        new_password = self._password_generator(cr, uid, context)
        customer_data = {}
        customer_data.update({'password':new_password})
        customer_data.update({'request_change_password':False})
        result = self.write(cr, uid, ids, customer_data, context=context)            
        if result:
            self._send_reset_password_notification(cr, uid, ids, context=context)
            _logger.info('Send Change Password Email Notification')        
        _logger.info('End Forget Password Process')
        
    def re_registration(self):
        _logger.info('Start Re-registration Process')
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)        

        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context=context)
        
        #Re-registration Validation
        if not rdm_customer_config.enable_re_registration:
            raise osv.except_osv(('Warning'), ('Customer Re-registration not enable'))
        if trans.re_registration:
            raise osv.except_osv(('Warning'), ('Customer already re-registration'))  
        if not trans.email_required:
            raise osv.except_osv(('Warning'), ('Customer Email Required'))
        if not trans.receive_email:
            raise osv.except_osv(('Warning'), ('Customer cannot Receive Email'))  
        
        #Generate Password    
        new_password = self._password_generator(cr, uid, context)
        customer_data = {}
        customer_data.update({'password':new_password})
        self.write(cr, uid, ids, customer_data, context=context)
        
        #Close Re-registration
        self._close_re_registration(cr, uid, ids, context)
        self._add_re_registration_point(cr, uid, ids, context)
    
        if rdm_config.enable_email:
            #Send Re-registration Email Notification
            self._send_re_registration_email_notification(cr, uid, ids, context=context)
                    
        _logger.info('End Re-registration Process')
        
    def _close_re_registration(self):
        _logger.info("Start Close Re-registration")                
        values = {}
        values.update({'re_registration':True})
        super(rdm_customer,self).write(cr, uid, ids, values, context=context)
        _logger.info("End Close Re-registration")    
        
    def reset_password(self):
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)    
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)        
        if not rdm_config.enable_email:
            raise osv.except_osv(('Warning'), ('Customer cannot Receive Email'))
        if not trans.receive_email:
            raise osv.except_osv(('Warning'), ('Customer cannot Receive Email'))                          
        new_password = self._password_generator(cr, uid, context)
        customer_data = {}
        customer_data.update({'password':new_password})
        self.write(cr, uid, ids, customer_data, context=context)
        self._send_reset_password_notification(cr, uid, ids, context=context)
        _logger.info('Send Change Password Email Notification')
                              
    def _password_generator(self, cr, uid ,context=None):
        size = 10
        chars= string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))
                
    def _add_new_member_point(self):
        _logger.info("Start Add New Member Point")                
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)                
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)            
        new_member_point = rdm_customer_config.new_member_point
        point_data = {}
        point_data.update({'customer_id': trans.id})            
        point_data.update({'trans_type': 'member'})
        point_data.update({'point':new_member_point})
        expired_date = datetime.today()+timedelta(rdm_customer_config.new_member_expired_duration)
        point_data.update({'expired_date': expired_date.strftime('%Y-%m-%d')})
        self.env('rdm.customer.point').create(cr, uid, point_data, context=context)
        _logger.info("End Add New Member Point")
    
    def _add_re_registration_point(self):
        _logger.info("Start Add Re-registration Point")
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)                
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)            
        re_registration_point = rdm_customer_config.re_registration_point
        point_data = {}
        point_data.update({'customer_id': trans.id})            
        point_data.update({'trans_type': 'member'})
        point_data.update({'point':re_registration_point})
        expired_date = datetime.today()+timedelta(rdm_customer_config.re_registration_expired_duration)
        point_data.update({'expired_date': expired_date.strftime('%Y-%m-%d')})
        self.env('rdm.customer.point').create(cr, uid, point_data, context=context)                    
        _logger.info("End Add Re-registration Point")
                
    def _add_referal_point(self):        
        _logger.info("Start Add Referal Point")
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)        
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)            
        referal_point = rdm_customer_config.referal_point
        point_data = {}
        point_data.update({'customer_id': trans.id})            
        point_data.update({'trans_type': 'reference'})
        point_data.update({'point':referal_point})
        expired_date = datetime.today()+timedelta(rdm_customer_config.expired_duration)
        point_data.update({'expired_date': expired_date.strftime('%Y-%m-%d')})
        self.env('rdm.customer.point').create(cr, uid, point_data, context=context)
        _logger.info("End Add Referal Point")
    
    
    def _new_member_process(self):
        _logger.info("Start New Member Process : " + str(ids[0]))
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
        customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)
        if customer_config.enable_new_member:            
            trans_id = ids[0]
            trans = self.get_trans(cr, uid, trans_id, context)
            if trans.email_required and trans.receive_email:                
                self._add_new_member_point(cr, uid, ids, context)
                                
            #Send Email
            if trans.email_required and trans.receive_email and rdm_config.enable_email:                        
                _logger.info('Send Email New Member')
                email_obj = self.env('email.template')        
                template_ids = customer_config.new_member_email_tmpl
                email = email_obj.browse(cr, uid, template_ids)  
                email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
                email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)                                                            
        _logger.info("End New Member Process")
        
    def _referal_process(self):
        _logger.info("Start Referal Process : " + str(ids[0]))
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
        customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)
        if customer_config.enable_referal:
            trans_id = ids[0]
            trans = self.get_trans(cr, uid, trans_id, context)
            if trans.ref_id:
                if trans.ref_id.email_required and trans.ref_id.receive_email:
                    self._add_referal_point(cr, uid, [trans.ref_id.id], context)
                
                #Send Email
                if trans.ref_id.email_required and trans.ref_id.receive_email and rdm_config.enable_email:                    
                    _logger.info('Send Email Referal')
                    email_obj = self.env('email.template')        
                    template_ids = customer_config.referal_email_tmpl
                    email = email_obj.browse(cr, uid, template_ids)  
                    email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
                    email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)           
            else:
                _logger.info('No Referal Point')    
        return True 
            
    def _check_duplicate(self, cr, uid, values, context=None):      
        _logger.info('Start Check Duplicate')
        customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)        
        #Check Email Address
        if customer_config.duplicate_email:
            if values.get('email_required'):
                                        
                if 'customer_id' in values.keys():
                    #Update Transaction
                    customer_ids = self.search(cr, uid, [('email','=',values.get('email')),('id','!=',values.get('customer_id'))], context=context)
                else:
                    #Create Transaction
                    customer_ids = self.search(cr, uid, [('email','=',values.get('email'))], context=context)
                    
                if customer_ids:
                    customer = self.browse(cr, uid, customer_ids, context=context)[0]
                    _logger.info('End Check Duplicate')
                    return True,'Email Duplicate with ' + customer.name
                
        #Check Social ID                            
        if customer_config.duplicate_social_id:
            customer_ids = self.search(cr, uid, [('social_id','=',values.get('social_id')),], context=context)
            if customer_ids:
                customer = self.browse(cr, uid, customer_ids, context=context)[0]
                _logger.info('End Check Duplicate')
                return True,'Social ID Duplicate with ' + customer.name  
            
        #check AYC Number
        if values.get('ayc_number'):
            customer_ids = self.search(cr, uid, [('ayc_number','=',values.get('ayc_number')),], context=context)        
            if customer_ids:
                customer = self.browse(cr, uid, customer_ids, context=context)[0]
                _logger.info('End Check Duplicate')
                return True,'Duplicate AYC Number with ' + customer.name
            
        _logger.info('End Check Duplicate')
        return False,'Not Duplicate' 
            
    def onchange_email_required(self, cr, uid, ods, email_required, context={}):
        if not email_required:            
            return {'value':{'email_required':''}}
                
    def onchange_mobil_phone1_number(self, cr, uid, ids, mobile_phone1, context={}):
        if not mobile_phone1:
            return {'value':{}}            
        return {'value':{'mobile_phone1':mobile_phone1}}
    
    def onchange_mobile_phone2_number(self, cr, uid, ids, mobile_phone2, context={}):
        if not mobile_phone2:
            return {'value':{}}                
        return {'value':{'mobile_phone2':mobile_phone2}}    
        
    def _send_email_notification(self, cr, uid, values, context=None):
        _logger.info('Start Send Email Notification')
        mail_mail = self.env('mail.mail')
        mail_ids = []
        mail_ids.append(mail_mail.create(cr, uid, {
            'email_from': values['email_from'],
            'email_to': values['email_to'],
            'subject': values['subject'],
            'body_html': values['body_html'],
            }, context=context))
        mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info('End Send Email Notification')          
            
    
    def send_create_email_notification(self):
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context=context)
        rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)                
        if rdm_config and rdm_config.enable_email and trans.receive_email:
            rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)
            if rdm_customer_config.enable_new_member:
                self.send_mail_to_new_customer(cr, uid, ids, context)
            if rdm_customer_config.enable_referal:
                self.send_mail_to_referal_customer(cr, uid, ids, context)
    
    def _send_re_registration_email_notification(self):
        _logger.info('Start Send Re-registraton Email Notification')
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)         
        email_obj = self.env('email.template')        
        template_ids = rdm_customer_config.re_registration_email_tmpl
        email = email_obj.browse(cr, uid, template_ids)  
        email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                'email_to': email.email_to,
                                                'subject': email.subject,
                                                'body_html': email.body_html,
                                                'email_recipients': email.email_recipients})
        email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)           
        _logger.info('End Send Re-registraton Email Notification')
        
    def _send_request_reset_password_notification(self):
        _logger.info('Start Send Request Reset Password Notification')
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)
        email_obj = self.env('email.template')        
        template_ids = rdm_customer_config.request_reset_password_email_tmpl
        email = email_obj.browse(cr, uid, template_ids)  
        email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                'email_to': email.email_to,
                                                'subject': email.subject,
                                                'body_html': email.body_html,
                                                'email_recipients': email.email_recipients})
        email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)
        
        _logger.info('End Send Request Reset Password Notification')
        
    def _send_reset_password_notification(self):
        _logger.info('Start Send Reset Password Notification')
        rdm_customer_config = self.env('rdm.customer.config').get_config(cr, uid, context=context)
        email_obj = self.env('email.template')        
        template_ids = rdm_customer_config.reset_password_email_tmpl
        email = email_obj.browse(cr, uid, template_ids)  
        email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                'email_to': email.email_to,
                                                'subject': email.subject,
                                                'body_html': email.body_html,
                                                'email_recipients': email.email_recipients})
        email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)
        _logger.info('Start End Reset Password Notification')
        
        
    _columns = {                    
        'type': fields.many2one('rdm.customer.type','Type'),        
        'contact_type': fields.selection(CONTACT_TYPES,'Contact Type',size=16),            
        'old_ayc_number': fields.char('Old AYC #', size=50),
        'ayc_number': fields.char('AYC #', size=50, required=True),        
        'name': fields.char('Name', size=200, required=True),
        'title': fields.many2one('rdm.tenant.title','Title'),        
        'birth_place': fields.char('Birth Place', size=100),
        'birth_date': fields.date('Birth Date', required=True),
        'gender': fields.many2one('rdm.customer.gender','Gender', required=True),
        'ethnic': fields.many2one('rdm.customer.ethnic','Ethnic'),
        'religion': fields.many2one('rdm.customer.religion','Religion'),
        'marital': fields.many2one('rdm.customer.marital','Marital'),
        'social_id': fields.char('ID or Passport', size=50, required=True),
        'address': fields.text('Address'),
        'province': fields.many2one('rdm.province','Province'),
        'city': fields.many2one('rdm.city','City'),
        'zipcode': fields.char('Zipcode', size=10),
        'phone1': fields.char('Phone 1', size=20),
        'phone2': fields.char('Phone 2', size=20),
        'mobile_phone1': fields.char('Mobile Phone 1', size=20, required=True),
        'mobile_phone2': fields.char('Mobile Phone 2', size=20),                
        'email': fields.char('Email',size=100),
        'email_required': fields.boolean('Email Required'),
        'password': fields.char('Password',size=20),
        'request_change_password': fields.boolean('Request Change Password'),
        'request_change_password_passcode': fields.char('Passcode', size=50),
        'request_change_password_expired': fields.datetime('Passcode Expired Time'),
        'request_change_password_times': fields.integer('Request Change Passwosrd Times'),            
        'zone': fields.many2one('rdm.customer.zone','Residential Zone'),
        'occupation': fields.many2one('rdm.customer.occupation','Occupation'),
        'education': fields.many2one('rdm.customer.education', 'Education'),
        'card_type': fields.many2one('rdm.card.type', 'Card Type',),
        'interest': fields.many2one('rdm.customer.interest','Interest'),
        'ref_id': fields.many2one('rdm.customer','Refferal'),
        'receive_email': fields.boolean('Receive Email'),        
        'join_date': fields.date('Join Date'),           
        're_registation': fields.boolean('Re-registration'),           
        're_registration': fields.boolean('Re-registration', readonly=True),              
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),    
        'deleted': fields.boolean('Deleted',readonly=True),       
        'create_uid': fields.many2one('res.users','Created By', readonly=True),
        'create_date': fields.datetime('Date Created', readonly=True),
        'write_uid': fields.many2one('res.users','Modified By', readonly=True),
        'write_date': fields.datetime('Date Modified', readonly=True),
    }
    
    _defaults = {
         'contact_type': lambda *a : 'customer',
         'email_required': lambda *a: True,         
         'join_date': fields.date.context_today,              
         'request_change_password': lambda *a: False,
         'request_change_password_times': lambda *a: 0, 
         're_registation': lambda *a: False,
         'zone': lambda *a: 29,
         'state': lambda *a: 'draft',
         'deleted': lambda *a: False,      
    }
    
    def create(self, cr, uid, values, context=None):
        
        if 'email_required' in values.keys() and 'receive_email' in values.keys():            
            if values.get('email_required') and values.get('receive_email'):            
                values.update({'re_registration': True})
            
        #Upper Case Name
        if 'name' in values.keys():
            name = values.get('name')
            values.update({'name':name.upper()})
        
        if values['contact_type'] == 'tenant':
            if 'tenant_id' in values.keys():                        
                tenant_id = values['tenant_id']
                if tenant_id:
                    values.update({'contact_type': 'tenant'})
        
        #Lower Case Email    
        if 'email' in values.keys():
            email = values.get('email')
            if email:
                values.update({'email':email.lower()})
            
        #Mobile Phone 1          
        if 'mobile_phone1' in values.keys():            
            mobile_phone1 = values.get('mobile_phone1')
            if mobile_phone1:
                if mobile_phone1[0:2] == '62':
                    values.update({'mobile_phone1':mobile_phone1})
                elif mobile_phone1[0] == '0':
                    mobile_phone1 = '62' + mobile_phone1[1:len(mobile_phone1)-1]                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 1 format should be start with +62 or 0'))       

        #Mobile Phone 1        
        if 'mobile_phone2' in values.keys():            
            mobile_phone2 = values.get('mobile_phone2')
            if mobile_phone2:
                if mobile_phone2[0:2] == '62':
                    values.update({'mobile_phone2':mobile_phone2})
                elif mobile_phone2[0] == '0':
                    mobile_phone2 = '62' + mobile_phone2[1:len(mobile_phone2)-1]                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 2 format should be start with +62 or 0'))       
        
        #Generate Password        
        values.update({'password':self._password_generator(cr, uid, context=context)})
        
        #Checks Duplicate Customer
        is_duplicate, message = self._check_duplicate(cr, uid ,values, context=context)

        if is_duplicate:
            raise osv.except_osv(('Warning'), (message))
        else:                           
            #Create Customer         
            id =  super(rdm_customer, self).create(cr, uid, values, context=context)
                
            #Enable Customer
            self.set_enable(cr, uid, [id], context)
            
            #Process New Member and Generate Point if Enable
            self._new_member_process(cr, uid, [id], context)
            
            #Process Referal and Generate Point For Reference Customer If Enable
            self._referal_process(cr, uid, [id], context)
            
            #Send Email Notification for Congrat and Customer Web Access Password
            #self.send_create_email_notification(cr, uid, [id], context)
                        
            return id 
        
    def write(self, cr, uid, ids, values, context=None):
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)
                
        if 'state' in values.keys():
            state = values.get('state') 
            #Request Change Password
            if state == 'request_change_password':
                self._request_forget_password(cr, uid, ids, context)
                return True
            if state == 'reset_password':
                self._forget_password(cr, uid, ids, context)
                return True
            
        #Upper Case Name
        if 'name' in values.keys():
            name = values.get('name')
            values.update({'name':name.upper()})

        #Lower Case Email
        if 'email' in values.keys():
            email = values.get('email')
            if email:                
                values.update({'email_required': True})
                values.update({'email':email.lower()}) 
                                            
        #Mobile Phone 1        
        if 'mobile_phone1' in values.keys():            
            mobile_phone1 = values.get('mobile_phone1')
            if mobile_phone1:
                if mobile_phone1[0:2] == '62':
                    values.update({'mobile_phone1':mobile_phone1})
                elif mobile_phone1[0] == '0':
                    mobile_phone1 = '62' + mobile_phone1[1:len(mobile_phone1)-1]
                    values.update({'mobile_phone1':mobile_phone1})                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 1 format should be start with +62 or 0'))       

        #Mobile Phone 1        
        if 'mobile_phone2' in values.keys():            
            mobile_phone2 = values.get('mobile_phone2')
            if mobile_phone2:
                if mobile_phone2[0:2] == '62':
                    values.update({'mobile_phone2':mobile_phone2})
                elif mobile_phone2[0] == '0':
                    mobile_phone2 = '62' + mobile_phone2[1:len(mobile_phone2)-1]
                    values.update({'mobile_phone2':mobile_phone2})                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 2 format should be start with +62 or 0'))       
        
        values.update({'customer_id': ids[0]})
        is_duplicate, message = self._check_duplicate(cr, uid, values, context=context)

        if is_duplicate:
            raise osv.except_osv(('Warning'), (message))
        else:
            return super(rdm_customer,self).write(cr, uid, ids, values, context=context)
            
rdm_customer()

