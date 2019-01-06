from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class rdm_customer_config(models.Model):
    _name = "rdm.customer.config"
    _description = "Redemption Customer Config"
    
    def get_config(self):
        ids = self.search([("state","=", True),])
        if ids:
            return self.env("rdm.customer.config").browse(ids)
        else:
            return None

    enable_new_member = fields.Boolean("Enable New Member")
    new_member_email_tmpl = fields.Integer("New Member Email")
    new_member_point = fields.Integer("New Member Point")
    new_member_expired_duration = fields.Integer("New Member Expired Duration")
    enable_re_registration = fields.Boolean("Enable Re-registration")
    re_registration_email_tmpl = fields.Integer("Registration Email")
    re_registration_point = fields.Integer("Re-registration Point")
    re_registration_expired_duration = fields.Integer("Re-registration Expired Duration")
    enable_referal = fields.Boolean("Enable Referal", default=False)
    referal_email_tmpl = fields.Integer("Referral Email")
    referal_point = fields.Integer("Referal Point", default=0)
    expired_duration = fields.Integer("Expired Duration", default=0)
    request_reset_password_email_tmpl = fields.Integer("Request Reset Password Email")
    reset_password_email_tmpl = fields.Integer("Reset Password Email")
    duplicate_email = fields.Boolean("Duplicate Email")
    duplicate_social_id = fields.Boolean("Duplicate Social ID")
    state = fields.Boolean("Status", default=True)


class rdm_customer_config_settings(models.Model):
    _name = "rdm.customer.config.settings"
    _inherit = "res.config.settings"
    
    enable_new_member = fields.Boolean("Enable New Member")
    new_member_email_tmpl = fields.Many2one("email.template","New Member Email")
    new_member_point = fields.Integer("New Member Point")
    new_member_expired_duration = fields.Integer("New Member Expired Duration")
    enable_re_registration = fields.Boolean("Enable Re-registration")
    re_registration_email_tmpl = fields.Many2one("email.template","Registration Email")
    re_registration_point = fields.Integer("Re-registration Point")
    re_registration_expired_duration = fields.Integer("Re-registration Expired Duration")
    enable_referal = fields.Boolean("Enable Referal")
    referal_email_tmpl = fields.Many2one("email.template","Referral Email")
    referal_point = fields.Integer("Referal Point")
    expired_duration = fields.Integer("Expired Duration")
    request_reset_password_email_tmpl = fields.Many2one("email.template","Request Reset Password Email")
    reset_password_email_tmpl = fields.Many2one("email.template","Reset Password Email")
    duplicate_email = fields.Boolean("Duplicate Email")
    duplicate_social_id = fields.Boolean("Duplicate Social ID")


    def get_default_enable_new_member(self):
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            enable_new_member = self.env("rdm.customer.config").browse( ids)
        else: 
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            enable_new_member = False
        return {"enable_new_member": enable_new_member}

    def set_default_enable_new_member(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        enable_new_member=config.enable_new_member
        self.env("rdm.customer.config").write( config_ids, {"enable_new_member": enable_new_member})

    def get_default_new_member_email_tmpl(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            new_member_email_tmpl = self.env("rdm.customer.config").browse( ids)
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            new_member_email_tmpl = 0
        return {"new_member_email_tmpl": new_member_email_tmpl}
    
    def set_default_new_member_email_tmpl(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        new_member_email_tmpl=config
        self.env("rdm.customer.config").write( config_ids, {"new_member_email_tmpl": new_member_email_tmpl})

    def get_default_new_member_point(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            new_member_point = self.env("rdm.customer.config").browse( ids).new_member_point
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            new_member_point = 0
        return {"new_member_point": new_member_point}
    
    def set_default_new_member_point(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        new_member_point=config.new_member_point
        self.env("rdm.customer.config").write( config_ids, {"new_member_point": new_member_point})
            
    def get_default_new_member_expired_duration(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            new_member_expired_duration = self.env("rdm.customer.config").browse( ids).new_member_expired_duration
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            new_member_expired_duration = 0
        return {"new_member_expired_duration": new_member_expired_duration}
    
    def set_default_new_member_expired_duration(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        new_member_expired_duration=config.new_member_expired_duration
        self.env("rdm.customer.config").write( config_ids, {"new_member_expired_duration": new_member_expired_duration})


    def get_default_enable_re_registration(self):
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            enable_re_registration = self.env("rdm.customer.config").browse( ids).enable_re_registration
        else: 
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            enable_re_registration = False
        return {"enable_re_registration": enable_re_registration}

    def set_default_enable_re_registration(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        enable_re_registration=config.enable_re_registration
        self.env("rdm.customer.config").write( config_ids, {"enable_re_registration": enable_re_registration})

    def get_default_re_registration_email_tmpl(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            re_registration_email_tmpl = self.env("rdm.customer.config").browse( ids).re_registration_email_tmpl
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            re_registration_email_tmpl = 0
        return {"re_registration_email_tmpl": re_registration_email_tmpl}
    
    def set_default_re_registration_email_tmpl(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        re_registration_email_tmpl=config.re_registration_email_tmpl
        self.env("rdm.customer.config").write( config_ids, {"re_registration_email_tmpl": re_registration_email_tmpl})

    def get_default_re_registration_point(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            re_registration_point = self.env("rdm.customer.config").browse( ids).re_registration_point
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            re_registration_point = 0
        return {"re_registration_point": re_registration_point}
    
    def set_default_re_registration_point(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        re_registration_point=config.re_registration_point
        self.env("rdm.customer.config").write( config_ids, {"re_registration_point": re_registration_point})
            
    def get_default_re_registration_expired_duration(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            re_registration_expired_duration = self.env("rdm.customer.config").browse( ids).re_registration_expired_duration
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            re_registration_expired_duration = 0
        return {"re_registration_expired_duration": re_registration_expired_duration}
    
    def set_default_re_registration_expired_duration(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        re_registration_expired_duration=config.re_registration_expired_duration
        self.env("rdm.customer.config").write( config_ids, {"re_registration_expired_duration": re_registration_expired_duration})



    def get_default_enable_referal(self):
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            enable_referal = self.env("rdm.customer.config").browse( ids).enable_referal
        else: 
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            enable_referal = False
        return {"enable_referal": enable_referal}


    def set_default_enable_referal(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        enable_referal=config.enable_referal
        self.env("rdm.customer.config").write( config_ids, {"enable_referal": enable_referal})

    def get_default_referal_email_tmpl(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            referal_email_tmpl = self.env("rdm.customer.config").browse( ids).referal_email_tmpl
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            referal_email_tmpl = 0
        return {"referal_email_tmpl": referal_email_tmpl}
    
    def set_default_referal_email_tmpl(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        referal_email_tmpl=config.referal_email_tmpl
        self.env("rdm.customer.config").write( config_ids, {"referal_email_tmpl": referal_email_tmpl})
        
    def get_default_referal_point(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            referal_point = self.env("rdm.customer.config").browse( ids).referal_point
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            referal_point = 0
        return {"referal_point": referal_point}
    
    def set_default_referal_point(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        referal_point=config.referal_point
        self.env("rdm.customer.config").write( config_ids, {"referal_point": referal_point})
        
        
    def get_default_expired_duration(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            expired_duration = self.env("rdm.customer.config").browse( ids).expired_duration
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            expired_duration = 0
        return {"expired_duration": expired_duration}
    
    def set_default_expired_duration(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        expired_duration=config.expired_duration
        self.env("rdm.customer.config").write( config_ids, {"expired_duration": expired_duration})
        

    def get_default_request_reset_password_email_tmpl(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            request_reset_password_email_tmpl = self.env("rdm.customer.config").browse( ids).request_reset_password_email_tmpl
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            request_reset_password_email_tmpl = 0
        return {"request_reset_password_email_tmpl": request_reset_password_email_tmpl}
    
    def set_default_request_reset_password_email_tmpl(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        request_reset_password_email_tmpl=config.request_reset_password_email_tmpl
        self.env("rdm.customer.config").write( config_ids, {"request_reset_password_email_tmpl": request_reset_password_email_tmpl})
        
    def get_default_reset_password_email_tmpl(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            reset_password_email_tmpl = self.env("rdm.customer.config").browse( ids).reset_password_email_tmpl
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            reset_password_email_tmpl = 0
        return {"reset_password_email_tmpl": reset_password_email_tmpl}
    
    def set_default_reset_password_email_tmpl(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        reset_password_email_tmpl=config.reset_password_email_tmpl
        self.env("rdm.customer.config").write( config_ids, {"reset_password_email_tmpl": reset_password_email_tmpl})
        
    def get_default_duplicate_email(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            duplicate_email = self.env("rdm.customer.config").browse( ids).duplicate_email
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            duplicate_email = False
        return {"duplicate_email": duplicate_email}
    
    def set_default_duplicate_email(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        self.env("rdm.customer.config").write( config_ids, {"duplicate_email": self.duplicate_email})
        
    
    def get_default_duplicate_social_id(self):    
        ids = self.env("rdm.customer.config").search( [("state","=", True),])
        if ids:
            duplicate_social_id = self.env("rdm.customer.config").browse( ids).duplicate_social_id
        else:
            customer_data = {}
            result_id = self.env("rdm.customer.config").create( customer_data)
            duplicate_social_id = False
        return {"duplicate_social_id": duplicate_social_id}
    
    def set_default_duplicate_social_id(self):
        config_ids = self.env("rdm.customer.config").search( [("state","=", True),])
        config = self.browse( ids, context)
        duplicate_social_id=config.duplicate_social_id
        self.env("rdm.customer.config").write( config_ids, {"duplicate_social_id": duplicate_social_id})
