from odoo import api, fields, models
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError, Warning
import logging
import re
import logging
import string
import random
import uuid

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [
    ("draft","New"),    
    ("active","Active"),    
    ("blacklist","Black List"),    
    ("disable", "Disable"),
]

CONTACT_TYPES = [
    ("customer","Customer"),
    ("tenant","Tenant"),
    ("both","Customer or Tenant"),    
]


# class rdm_customer_change_password(models.Model):
# #     _name = "rdm.customer.change.password"
# #     _description = "Redemption Customer Change Password"
# #
# #     def change_password(self):
# #
# #         customer_id = self.customer_id
# #         data = {}
# #         if self.password_new == self.password_confirm:
# #             data.update({"password":self.password_new})
# #             self.env("rdm.customer").write( [customer_id], data)
# #         return True
# #
# #
# #     password_new = fields.Char("New Password", ),
# #     password_confirm = fields.Text("Confirm Password", )


class rdm_customer(models.Model):
    _name = "rdm.customer"
    _description = "Redemption Customer"

    # @api.one
    # def set_black_list(self):
    #     _logger.info("Blacklist ID : " + str(self.id))
    #     self.write({"state": "blacklist"})
    #     return True
    #
    # @api.one
    # def set_remove_black_list(self):
    #     _logger.info("Reset Blacklist ID : " + str(self.id))
    #     self.write({"state": "active"})
    #     return True

    @api.one
    def set_disable(self):
        self.state = "disable"


    @api.one
    def set_enable(self):
        self.state = "active"

    #
    # @api.one
    # def get_trans(self):
    #     return self.browse(self.trans_id);
    #
    # @api.one
    # def change_password(self):
    #     return {
    #            "type": "ir.actions.act_window",
    #            "name": "Change Password",
    #            "view_mode": "form",
    #            "view_type": "form",
    #            "res_model": "rdm.customer.change.password",
    #            "nodestroy": True,
    #            "target":"new",
    #            "context": {"customer_id": self.id},
    #     }
    #
    # @api.one
    # def _request_forget_password(self):
    #     _logger.info("Start Request Forget Password Process")
    #     values = {}
    #     values.update({"request_change_password": True})
    #     values.update({"request_change_password_passcode": str(uuid.uuid1()).replace("-","")})
    #     result = super(rdm_customer, self).write( values)
    #     if result:
    #         self._send_request_reset_password_notification()
    #     _logger.info("End Request Forget Password Process")
    #
    # @api.one
    # def _forget_password(self):
    #     _logger.info("Start Forget Password Process")
    #     rdm_config = self.env("rdm.config")
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #
    #     if not rdm_config.enable_email:
    #         raise ValidationError(("Warning"), ("Customer cannot Receive Email"))
    #
    #     if not trans.receive_email:
    #         raise ValidationError(("Warning"), ("Customer cannot Receive Email"))
    #
    #     new_password = self._password_generator()
    #     customer_data = {}
    #     customer_data.update({"password":new_password})
    #     customer_data.update({"request_change_password":False})
    #     result = self.write(customer_data)
    #     if result:
    #         self._send_reset_password_notification()
    #         _logger.info("Send Change Password Email Notification")
    #     _logger.info("End Forget Password Process")
    #
    # @api.one
    # def re_registration(self):
    #     _logger.info("Start Re-registration Process")
    #     rdm_config = self.env("rdm.config")
    #     rdm_customer_config = self.env("rdm.customer.config")
    #
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #
    #     #Re-registration Validation
    #     if not rdm_customer_config.enable_re_registration:
    #         raise ValidationError(("Warning"), ("Customer Re-registration not enable"))
    #     if trans.re_registration:
    #         raise ValidationError(("Warning"), ("Customer already re-registration"))
    #     if not trans.email_required:
    #         raise ValidationError(("Warning"), ("Customer Email Required"))
    #     if not trans.receive_email:
    #         raise ValidationError(("Warning"), ("Customer cannot Receive Email"))
    #
    #     #Generate Password
    #     new_password = self._password_generator()
    #     customer_data = {}
    #     customer_data.update({"password":new_password})
    #     self.write(customer_data)
    #
    #     #Close Re-registration
    #     self._close_re_registration()
    #     self._add_re_registration_point()
    #
    #     if rdm_config.enable_email:
    #         #Send Re-registration Email Notification
    #         self._send_re_registration_email_notification()
    #
    #     _logger.info("End Re-registration Process")
    #
    # @api.one
    # def _close_re_registration(self):
    #     _logger.info("Start Close Re-registration")
    #     values = {}
    #     values.update({"re_registration":True})
    #     super(rdm_customer,self).write( values)
    #     _logger.info("End Close Re-registration")
    #
    # @api.one
    # def reset_password(self):
    #     rdm_config = self.env("rdm.config")
    #     rdm_customer_config = self.env["rdm.customer.config"]
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #     if not rdm_config.enable_email:
    #         raise ValidationError(("Warning"), ("Customer cannot Receive Email"))
    #     if not trans.receive_email:
    #         raise ValidationError(("Warning"), ("Customer cannot Receive Email"))
    #     new_password = self._password_generator()
    #     customer_data = {}
    #     customer_data.update({"password":new_password})
    #     self.write(customer_data)
    #     self._send_reset_password_notification()
    #     _logger.info("Send Change Password Email Notification")
    #
    @api.one
    def _password_generator(self):
        size = 10
        chars= string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(size))
    #
    # @api.one
    # def _add_new_member_point(self):
    #     _logger.info("Start Add New Member Point")
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #     new_member_point = rdm_customer_config.new_member_point
    #     point_data = {}
    #     point_data.update({"customer_id": trans.id})
    #     point_data.update({"trans_type": "member"})
    #     point_data.update({"point":new_member_point})
    #     expired_date = datetime.today()+timedelta(rdm_customer_config.new_member_expired_duration)
    #     point_data.update({"expired_date": expired_date.strftime("%Y-%m-%d")})
    #     self.env("rdm.customer.point").create( point_data)
    #     _logger.info("End Add New Member Point")
    #
    # @api.one
    # def _add_re_registration_point(self):
    #     _logger.info("Start Add Re-registration Point")
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #     re_registration_point = rdm_customer_config.re_registration_point
    #     point_data = {}
    #     point_data.update({"customer_id": trans.id})
    #     point_data.update({"trans_type": "member"})
    #     point_data.update({"point":re_registration_point})
    #     expired_date = datetime.today()+timedelta(rdm_customer_config.re_registration_expired_duration)
    #     point_data.update({"expired_date": expired_date.strftime("%Y-%m-%d")})
    #     self.env("rdm.customer.point").create( point_data)
    #     _logger.info("End Add Re-registration Point")
    #
    # @api.one
    # def _add_referal_point(self):
    #     _logger.info("Start Add Referal Point")
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     referal_point = rdm_customer_config.referal_point
    #     point_data = {}
    #     point_data.update({"customer_id": trans.id})
    #     point_data.update({"trans_type": "reference"})
    #     point_data.update({"point":referal_point})
    #     expired_date = datetime.today()+timedelta(rdm_customer_config.expired_duration)
    #     point_data.update({"expired_date": expired_date.strftime("%Y-%m-%d")})
    #     self.env("rdm.customer.point").create( point_data)
    #     _logger.info("End Add Referal Point")
    #
    # @api.one
    # def _new_member_process(self):
    #     _logger.info("Start New Member Process : " + str(self.id))
    #     rdm_config = self.env("rdm.config")
    #     customer_config = self.env("rdm.customer.config")
    #     if customer_config.enable_new_member:
    #         trans_id = self.id
    #         trans = self.get_trans( trans_id)
    #         if trans.email_required and trans.receive_email:
    #             self._add_new_member_point()
    #
    #         #Send Email
    #         if trans.email_required and trans.receive_email and rdm_config.enable_email:
    #             _logger.info("Send Email New Member")
    #             email_obj = self.env("email.template")
    #             template_ids = customer_config.new_member_email_tmpl
    #             email = email_obj.browse( template_ids)
    #             email_obj.write({"email_from": email.email_from,
    #                                                 "email_to": email.email_to,
    #                                                 "subject": email.subject,
    #                                                 "body_html": email.body_html,
    #                                                 "email_recipients": email.email_recipients})
    #             email_obj.send_mail( template_ids, self.id, True)
    #     _logger.info("End New Member Process")
    #
    # @api.one
    # def _referal_process(self):
    #     _logger.info("Start Referal Process : " + str(self.id))
    #     rdm_config = self.env("rdm.config")
    #     customer_config = self.env("rdm.customer.config")
    #     if customer_config.enable_referal:
    #         trans = self.trans_id
    #         if trans.ref_id:
    #             if trans.ref_id.email_required and trans.ref_id.receive_email:
    #                 self._add_referal_point( [trans.ref_id.id])
    #
    #             #Send Email
    #             if trans.ref_id.email_required and trans.ref_id.receive_email and rdm_config.enable_email:
    #                 _logger.info("Send Email Referal")
    #                 email_obj = self.env("email.template")
    #                 template_ids = customer_config.referal_email_tmpl
    #                 email = email_obj.browse( template_ids)
    #                 email_obj.write({"email_from": email.email_from,
    #                                                 "email_to": email.email_to,
    #                                                 "subject": email.subject,
    #                                                 "body_html": email.body_html,
    #                                                 "email_recipients": email.email_recipients})
    #                 email_obj.send_mail( template_ids, trans.id, True)
    #         else:
    #             _logger.info("No Referal Point")
    #     return True
    #
    # @api.one
    # def _check_duplicate(self, vals):
    #     _logger.info("Start Check Duplicate")
    #     # customer_config = self.env["rdm.customer.config"]
    #     #Check Email Address
    #     # if customer_config.duplicate_email:
    #     if vals['email_required']:
    #
    #         if "customer_id" in self.keys():
    #             #Update Transaction
    #             customer_ids = self.search( [("email","=",self.email),("id","!=",self.customer_id)])
    #         else:
    #             #Create Transaction
    #             customer_ids = self.search( [("email","=",self.email)])
    #
    #         if customer_ids:
    #             customer = self.browse( customer_ids)[0]
    #             _logger.info("End Check Duplicate")
    #             return True,"Email Duplicate with " + customer.name

    #     #Check Social ID
    #     if customer_config.duplicate_social_id:
    #         customer_ids = self.search( [("social_id","=",self.social_id),])
    #         if customer_ids:
    #             customer = self.browse( customer_ids)[0]
    #             _logger.info("End Check Duplicate")
    #             return True,"Social ID Duplicate with " + customer.name
    #
    #     #check AYC Number
    #     if self.ayc_number:
    #         customer_ids = self.search( [("ayc_number","=",self.ayc_number),])
    #         if customer_ids:
    #             customer = self.browse( customer_ids)[0]
    #             _logger.info("End Check Duplicate")
    #             return True,"Duplicate AYC Number with " + customer.name
    #
    #     _logger.info("End Check Duplicate")
    #     return False,"Not Duplicate"
    #
    # @api.one
    # def onchange_email_required(self):
    #     if not self.email_required:
    #         return {"value":{"email_required":""}}
    #
    # @api.one
    # def onchange_mobil_phone1_number(self):
    #     if not self.mobile_phone1:
    #         return {"value":{}}
    #     return {"value":{"mobile_phone1": self.mobile_phone1}}
    #
    # @api.one
    # def onchange_mobile_phone2_number(self):
    #     if not self.mobile_phone2:
    #         return {"value":{}}
    #     return {"value":{"mobile_phone2": self.mobile_phone2}}
    #
    # @api.one
    # def _send_email_notification(self):
    #     _logger.info("Start Send Email Notification")
    #     mail_mail = self.env("mail.mail")
    #     mail_ids = []
    #     mail_ids.append(mail_mail.create( {
    #         "email_from": self.email_from,
    #         "email_to": self.email_to,
    #         "subject": self.subject,
    #         "body_html": self.body_html,
    #         }))
    #     mail_mail.send( mail_ids)
    #     _logger.info("End Send Email Notification")
    #
    # @api.one
    # def send_create_email_notification(self):
    #     trans_id = self.id
    #     trans = self.get_trans( trans_id)
    #     rdm_config = self.env("rdm.config")
    #     if rdm_config and rdm_config.enable_email and trans.receive_email:
    #         rdm_customer_config = self.env("rdm.customer.config")
    #         if rdm_customer_config.enable_new_member:
    #             self.send_mail_to_new_customer()
    #         if rdm_customer_config.enable_referal:
    #             self.send_mail_to_referal_customer()
    #
    # @api.one
    # def _send_re_registration_email_notification(self):
    #     _logger.info("Start Send Re-registraton Email Notification")
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     email_obj = self.env("email.template")
    #     template_ids = rdm_customer_config.re_registration_email_tmpl
    #     email = email_obj.browse( template_ids)
    #     email_obj.write( template_ids, {"email_from": email.email_from,
    #                                             "email_to": email.email_to,
    #                                             "subject": email.subject,
    #                                             "body_html": email.body_html,
    #                                             "email_recipients": email.email_recipients})
    #     email_obj.send_mail( template_ids, self.id, True)
    #     _logger.info("End Send Re-registraton Email Notification")
    #
    # @api.one
    # def _send_request_reset_password_notification(self):
    #     _logger.info("Start Send Request Reset Password Notification")
    #
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     email_obj = self.env("email.template")
    #
    #     template_ids = rdm_customer_config.request_reset_password_email_tmpl
    #     email = email_obj.browse( template_ids)
    #
    #     email_obj.write( template_ids, {"email_from": email.email_from,
    #                                             "email_to": email.email_to,
    #                                             "subject": email.subject,
    #                                             "body_html": email.body_html,
    #                                             "email_recipients": email.email_recipients})
    #     email_obj.send_mail( template_ids, self.id, True)
    #
    #     _logger.info("End Send Request Reset Password Notification")
    #
    # @api.one
    # def _send_reset_password_notification(self):
    #     _logger.info("Start Send Reset Password Notification")
    #
    #     rdm_customer_config = self.env("rdm.customer.config")
    #     email_obj = self.env("email.template")
    #
    #     template_ids = rdm_customer_config.reset_password_email_tmpl
    #     email = email_obj.browse(template_ids)
    #     email_obj.write( template_ids, {"email_from": email.email_from,
    #                                             "email_to": email.email_to,
    #                                             "subject": email.subject,
    #                                             "body_html": email.body_html,
    #                                             "email_recipients": email.email_recipients})
    #     email_obj.send_mail( template_ids, self.id, True)
    #     _logger.info("Start End Reset Password Notification")
        
        
                        
    type = fields.Many2one(comodel_name="rdm.customer.type", string="Type")
    contact_type = fields.Selection(selection=CONTACT_TYPES, string="Contact Type", size=16, default="customer")
    old_ayc_number = fields.Char(string="Old AYC #", size=50)
    ayc_number = fields.Char(string="AYC #", size=50, required=True)
    name = fields.Char(string="Name", size=200, required=True)
    title = fields.Many2one(comodel_name="rdm.tenant.title", string="Title")
    birth_place = fields.Char(comodel_name="Birth Place", size=100)
    birth_date = fields.Date(comodel_name="Birth Date", required=True)
    gender = fields.Many2one(comodel_name="rdm.customer.gender", string="Gender", required=True)
    ethnic = fields.Many2one(comodel_name="rdm.customer.ethnic", string="Ethnic")
    religion = fields.Many2one(comodel_name="rdm.customer.religion", string="Religion")
    marital = fields.Many2one(comodel_name="rdm.customer.marital", string="Marital")
    social_id = fields.Char(string="ID or Passport", size=50, required=True)
    address = fields.Text(string="Address")
    province = fields.Many2one(comodel_name="rdm.province", string="Province")
    city = fields.Many2one("rdm.city","City")
    zipcode = fields.Char(string="Zipcode", size=10)
    phone1 = fields.Char(string="Phone 1", size=20)
    phone2 = fields.Char(string="Phone 2", size=20)
    mobile_phone1 = fields.Char(string="Mobile Phone 1", size=20, required=True)
    mobile_phone2 = fields.Char(string="Mobile Phone 2", size=20)
    email = fields.Char("Email",size=100)
    email_required = fields.Boolean(string="Email Required", default=True)
    password = fields.Char(string="Password",size=20)
    request_change_password = fields.Boolean(string="Request Change Password", default=False)
    request_change_password_passcode = fields.Char(string="Passcode", size=50)
    request_change_password_expired = fields.Datetime(string="Passcode Expired Time")
    request_change_password_times = fields.Integer(string="Request Change Passwosrd Times", default=0)
    zone = fields.Many2one(comodel_name="rdm.customer.zone",string="Residential Zone",)
    occupation = fields.Many2one(comodel_name="rdm.customer.occupation",string="Occupation")
    education = fields.Many2one(comodel_name="rdm.customer.education", string="Education")
    card_type = fields.Many2one(comodel_name="rdm.card.type", string="Card Type",)
    interest = fields.Many2one(comodel_name="rdm.customer.interest", string="Interest")
    ref_id = fields.Many2one(comodel_name="rdm.customer", string="Refferal")
    receive_email = fields.Boolean(string="Receive Email")
    join_date = fields.Date(string="Join Date", default=fields.Datetime().now())
    re_registation = fields.Boolean(string="Re-registration", default=False)
    re_registration = fields.Boolean(string="Re-registration", readonly=True)
    state = fields.Selection(selection=AVAILABLE_STATES, string="Status", size=16, readonly=True, default="draft")
    deleted = fields.Boolean(string="Deleted",readonly=True, default=False)
    create_uid = fields.Many2one(comodel_name="res.users",string="Created By", readonly=True)
    create_date = fields.Datetime(string="Date Created", readonly=True)
    write_uid = fields.Many2one(comodel_name="res.users", string="Modified By", readonly=True)
    write_date = fields.Datetime(string="Date Modified", readonly=True)

    _sql_constraints = [('email_unique', 'unique(email,)', 'Email already exists.')]

    @api.model
    def create(self, vals):
        vals['state'] = "active"


        if "email_required" in vals.keys() and "receive_email" in vals.keys():
            if vals['email_required'] and vals['receive_email']:
                vals.update({"re_registration": True})

        #Upper Case Name
        if "name" in vals.keys():
            name = vals['name']
            vals.update({"name":name.upper()})

        # if vals['contact_type'] == "tenant":
        #     if "tenant_id" in vals.keys():
        #         vals.update({"contact_type": "tenant"})

        #Lower Case Email
        if "email" in vals.keys():
            email = vals['email']
            if email:
                vals.update({"email":email.lower()})
        else:
            vals.update({"email": self._password_generator()})

        #Mobile Phone 1
        if "mobile_phone1" in vals.keys():
            mobile_phone1 = vals['mobile_phone1']
            if mobile_phone1:
                if mobile_phone1[0:2] == "62":
                    vals.update({"mobile_phone1": mobile_phone1})
                elif mobile_phone1[0] == "0":
                    mobile_phone1 = "62" + mobile_phone1[1:len(mobile_phone1)-1]
                else:
                    raise ValidationError("Mobile Phone 1 format should be start with 62 or 0")

        #Mobile Phone 1
        if "mobile_phone2" in vals.keys():
            mobile_phone2 = vals['mobile_phone2']
            if mobile_phone2:
                if mobile_phone2[0:2] == "62":
                    vals.update({"mobile_phone2":mobile_phone2})
                elif mobile_phone2[0] == "0":
                    mobile_phone2 = "62" + mobile_phone2[1:len(mobile_phone2)-1]
                else:
                    raise ValidationError("Mobile Phone 2 format should be start with 62 or 0")

        # Generate Password

        vals.update({"password": self._password_generator()})

        #Checks Duplicate Customer
        # is_duplicate, message = self._check_duplicate()

        # if is_duplicate:
        #     raise ValidationError(("Warning"), (message))
        # else:
            # Create Customer
        id =  super(rdm_customer, self).create(vals)
        #
        #     #Enable Customer
        #     self.set_enable()
        #
        #     #Process New Member and Generate Point if Enable
        #     self._new_member_process()
        #
        #     #Process Referal and Generate Point For Reference Customer If Enable
        #     self._referal_process()
        #
        #     #Send Email Notification for Congrat and Customer Web Access Password
        #     #self.send_create_email_notification( [id])
        #
        return id
    #
    # @api.multi
    # def write(self, vals):
    #     trans_id = self.id
    #     trans = self.get_trans()
    #     values = {}
    #
    #     if "state" in self.keys():
    #         state = self.state
    #         #Request Change Password
    #         if state == "request_change_password":
    #             self._request_forget_password()
    #             return True
    #         if state == "reset_password":
    #             self._forget_password()
    #             return True
    #
    #     #Upper Case Name
    #     if "name" in values.keys():
    #         name = self.name
    #         values.update({"name":name.upper()})
    #
    #     #Lower Case Email
    #     if "email" in values.keys():
    #         email = self.email
    #         if email:
    #             values.update({"email_required": True})
    #             values.update({"email":email.lower()})
    #
    #     #Mobile Phone 1
    #     if "mobile_phone1" in values.keys():
    #         mobile_phone1 = self.mobile_phone1
    #         if mobile_phone1:
    #             if mobile_phone1[0:2] == "62":
    #                 values.update({"mobile_phone1":mobile_phone1})
    #             elif mobile_phone1[0] == "0":
    #                 mobile_phone1 = "62" + mobile_phone1[1:len(mobile_phone1)-1]
    #                 values.update({"mobile_phone1":mobile_phone1})
    #             else:
    #                 raise ValidationError(("Warning"), ("Mobile Phone 1 format should be start with +62 or 0"))
    #
    #     #Mobile Phone 1
    #     if "mobile_phone2" in values.keys():
    #         mobile_phone2 = self.mobile_phone2
    #         if mobile_phone2:
    #             if mobile_phone2[0:2] == "62":
    #                 values.update({"mobile_phone2":mobile_phone2})
    #             elif mobile_phone2[0] == "0":
    #                 mobile_phone2 = "62" + mobile_phone2[1:len(mobile_phone2)-1]
    #                 values.update({"mobile_phone2":mobile_phone2})
    #             else:
    #                 raise ValidationError(("Warning"), ("Mobile Phone 2 format should be start with +62 or 0"))
    #
    #     values.update({"customer_id": self.id})
    #     is_duplicate, message = self._check_duplicate(values)
    #
    #     if is_duplicate:
    #         raise ValidationError(("Warning"), (message))
    #     else:
    #         return super(rdm_customer,self).write(values)

