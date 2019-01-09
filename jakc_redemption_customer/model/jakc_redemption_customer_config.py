from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class rdm_customer_config_settings(models.Model):
    _inherit = "res.company"
    
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

