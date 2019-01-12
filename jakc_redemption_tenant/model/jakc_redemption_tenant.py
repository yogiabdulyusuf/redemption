from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ("draft","New"),    
    ("active","Active"),
    ("disable", "Disable"),
    ("terminate", "Terminate"),
]

AVAILABLE_PARTICIPANT = [
    ("1","AYC non participant tenant"),
    ("2","AYC participant tenant")
]

class rdm_tenant(models.Model):
    _name = "rdm.tenant"
    _description = "Redemption Tenant"

    @api.one
    def trans_reset(self):
        self.state = "active"
        return True

    @api.one
    def trans_disable(self):
        self.state = "disable"
        return True

    @api.one
    def trans_enable(self):
        self.state = "active"
        return True

    @api.one
    def trans_terminate(self):
        self.state = "terminate"
        return True

    @api.one
    def _get_trans(self):
        return self.trans_id
            

    name = fields.Char("Name", size=200, required=True)
    company = fields.Char("Company", size=200)
    category =  fields.Many2one("rdm.tenant.category","Category", required=True)
    grade =  fields.Many2one("rdm.tenant.grade","Grade", required=True)
    participant =  fields.Selection(AVAILABLE_PARTICIPANT,"Participant Type",required=True, default=1)
    location =  fields.Char("Location", size=10)
    floor =  fields.Char("Floor", size=10)
    number =  fields.Char("Number", size=10)
    start_Date =  fields.Date("Join Date", required=True)
    end_Date =  fields.Date("End Date")
    customer_ids =  fields.One2many("rdm.customer","tenant_id","Contacts")
    message_ids =  fields.One2many("rdm.tenant.message","tenant_id","Messages")
    state =  fields.Selection(AVAILABLE_STATES,"Status",size=16,readonly=True, default=draft)
    
    def create(self):
        values = {}
        values.upDate({"state" : "active"})
        trans_id = super(rdm_tenant,self).create(values)
        return trans_id

class rdm_tenant_message(models.Model):
    _name = "rdm.tenant.message"
    _description = "Redemption Tenant Message"
 
    trans_Date =  fields.Date("Date", required=True, default=fields.Datetime.now)
    tenant_id =  fields.Many2one("rdm.tenant","Tenant",required=True)
    customer_id =  fields.Many2one("rdm.customer","Contact",required=True)
    message_category_id =  fields.Many2one("rdm.tenant.message.category","Category",size=50,required=True)                     
    subject =  fields.Char("Subject",size=50,required=True)      
    message =  fields.Text("Message",required=True)
    state =  fields.Selection([("open","Open"),("reply","Reply"),("done","Close")],"State", default="open")


class rdm_tenant_message_category(models.Model):
    _name = "rdm.tenant.message.category"
    _description = "Redemption Tenant Message Category"

    name =  fields.Char("Name",size=100)
