from openerp.osv import fields, osv

SCHEMAS_SELECTIONS = [
    ('ethnic','Ethnic'),
    ('religion','Religion'),
    ('gender','Gender'),
    ('marital','Marital'),
    ('zone','Zone'),
    ('education','Education'),
    ('interest','Interest'),
    ('occupation','Occupation'),
    ('birthday','Birthday'),
    ('day','Day'),
    ('dayname','Day Name'),
    ('cardtype','Card Type'),
    ('tenant','Tenant'),
    ('tenanttype','Tenant Type'),
    ('bank','Bank'),
    ('bankcard','Bank Card'),
    ('age','Customer Age'),
    ('spending','Spending Amount'),
    ('participant','Participant Type'),
    ('cash','Cash'),    
]

OPERATOR_SELECTIONS = [
    ('eq','Equal'),
    ('ne','Not Equal'),
    ('lt','Less Than'),
    ('gt','Greater Than'),
    ('bw','Between'),
]

DAY_NAME_SELECTIONS = [
    ('01','Sunday'),
    ('02','Monday'),
    ('03','Tuesday'),
    ('04','Wednesday'),
    ('05','Thursday'),
    ('06','Friday'),
    ('07','Saturday')
]

OPERATION_SELECTIONS = [                    
    ('or','OR'),
    ('and','AND'),
]

AVAILABLE_PARTICIPANT = [
    ('1','AYC non participant tenant'),
    ('2','AYC participant tenant')
]

class rdm_rules(osv.osv):
    _name = "rdm.rules"
    _description = "Redemption Rules"
    _columns = {
        'name': fields.char('Name', size=200, required=True),
        'apply_for': fields.selection([('1','Coupon'),('2','Point'),('3','Reward')],'Apply For',required=True),
        'reward_id': fields.many2one('rdm.reward','Reward'),
        'operation': fields.selection([('add','Add'),('multiple','Multiple')],'Operation',required=True),
        'calculation': fields.selection([('terbesar','Terbesar'),('ditotal','Di Total')],'Method'),
        'quantity': fields.float('Quantity',required=True),
        'rules_detail_ids': fields.one2many('rdm.rules.detail','rules_id','Detail'),
    }
    
    _defaults = {
        'quantity': lambda *a : 1,
    }
    
rdm_rules()

class rdm_rules_detail(osv.osv):
    _name = "rdm.rules.detail"
    _description = "Redemption Rules Detail"
    _columns = {
        'rules_id': fields.many2one('rdm.rules','Rules'),
        'rule_schema': fields.selection(SCHEMAS_SELECTIONS,'Schema',required=True),
        'operation': fields.selection(OPERATION_SELECTIONS, 'Operation', required=True),                                               
        'day': fields.date('Day'),    
        'day_name': fields.selection(DAY_NAME_SELECTIONS,'Day Name'),
        'ethnic_ids': fields.one2many('rdm.rules.ethnic','rules_detail_id','Ethnic'),
        'religion_ids': fields.one2many('rdm.rules.religion','rules_detail_id','Religion'),
        'marital_ids': fields.one2many('rdm.rules.marital','rules_detail_id','Marital'),
        'zone_ids': fields.one2many('rdm.rules.zone','rules_detail_id','Zone'),
        'education_ids': fields.one2many('rdm.rules.education','rules_detail_id','Education'),
        'interest_ids': fields.one2many('rdm.rules.interest','rules_detail_id','Interest'),
        'occupation_ids': fields.one2many('rdm.rules.occupation','rules_detail_id','Occupation'),            
        'card_type_ids': fields.one2many('rdm.rules.card.type','rules_detail_id','Card Type'),
        'tenant_ids': fields.one2many('rdm.rules.tenant','rules_detail_id','Tenant'),
        'tenant_category_ids': fields.one2many('rdm.rules.tenant.category','rules_detail_id','Tenant Category'),
        'participant_ids': fields.one2many('rdm.rules.participant','rules_detail_id','Participant'),
        'bank_ids': fields.one2many('rdm.rules.bank','rules_detail_id','Bank'),        
        'bank_card_ids': fields.one2many('rdm.rules.bank.card','rules_detail_id','Bank Card'),
        'age_ids': fields.one2many('rdm.rules.customer.age','rules_detail_id','Age'),
        'spending_amount_ids': fields.one2many('rdm.rules.spending.amount','rules_detail_id','Spending Amount'),
        'gender_ids': fields.one2many('rdm.rules.gender','rules_detail_id','Gender'),
        'cash_ids': fields.one2many('rdm.rules.cash','rules_detail_id','Cash'),                                
    }
    _defaults = {
        'operation': lambda *a: 'and',
    }
    
rdm_rules_detail()


class rdm_rules_ethnic(osv.osv):
    _name = "rdm.rules.ethnic"
    _description = "Redemption Rule Ethnic"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'ethnic_id': fields.many2one('rdm.customer.ethnic','Ethnic'),
    }

rdm_rules_ethnic()

class rdm_rules_religion(osv.osv):
    _name = "rdm.rules.religion"
    _description = "Redemption Rule Religion"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'religion_id': fields.many2one('rdm.customer.religion','Religion'),
    }

rdm_rules_religion()

class rdm_rules_marital(osv.osv):
    _name = "rdm.rules.marital"
    _description = "Redemption Rule Marital"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'marital_id': fields.many2one('rdm.customer.marital','Marital'),
    }

rdm_rules_marital()

class rdm_rules_zone(osv.osv):
    _name = "rdm.rules.zone"
    _description = "Redemption Rule Zone"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'zone_id': fields.many2one('rdm.customer.zone','Zone'),
    }

rdm_rules_zone()

class rdm_rules_education(osv.osv):
    _name = "rdm.rules.education"
    _description = "Redemption Rule Education"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'education_id': fields.many2one('rdm.customer.education','Education'),
    }

rdm_rules_education()


class rdm_rules_interest(osv.osv):
    _name = "rdm.rules.interest"
    _description = "Redemption Rule Interest"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'interest_id': fields.many2one('rdm.customer.interest','Interest'),
    }

rdm_rules_interest()

class rdm_rules_occupation(osv.osv):
    _name = "rdm.rules.occupation"
    _description = "Redemption Rule Occupation"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'occupation_id': fields.many2one('rdm.customer.occupation','Occupation'),
    }

rdm_rules_occupation()


class rdm_rules_gender(osv.osv):
    _name = "rdm.rules.gender"
    _description = "Redemption Rule Gender"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'gender_id': fields.many2one('rdm.customer.gender','Gender'),
    }

rdm_rules_gender()

class rdm_rules_participant(osv.osv):
    _name = "rdm.rules.participant"
    _description = "Redemption Rule Tenant Participant Type"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'participant_id': fields.selection(AVAILABLE_PARTICIPANT,'Participant Type',required=True), 
    }

rdm_rules_participant()

class rdm_rules_card_type(osv.osv):
    _name = "rdm.rules.card.type"
    _description = "Redemption Rule Card Type"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'card_type_id': fields.many2one('rdm.card.type','Card Type')        
    }
    
rdm_rules_card_type()
    
class rdm_rules_tenant(osv.osv):
    _name = "rdm.rules.tenant"
    _description = "Redemption Rule Tenant"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'tenant_id': fields.many2one('rdm.tenant','Tenant') 
    }

rdm_rules_tenant()

class rdm_rules_customer_age(osv.osv):
    _name = "rdm.rules.customer.age"
    _description = "Redemption Rules Customer Age"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'operator': fields.selection(OPERATOR_SELECTIONS,'Operator',size=16,required=True),
        'value1': fields.integer('Value 01'),
        'value2': fields.integer('Value 02'),         
    }
    
rdm_rules_customer_age()

class rdm_rules_spending_amount(osv.osv):
    _name = "rdm.rules.spending.amount"
    _description = "Redemption Rules Spending Amount"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'operator': fields.selection(OPERATOR_SELECTIONS,'Operator',size=16,required=True),
        'value1': fields.float('Value 01'),
        'value2': fields.float('Value 02'),         
    }
    
rdm_rules_spending_amount()


class rdm_rules_tenant_category(osv.osv):
    _name = "rdm.rules.tenant.category"
    _description = "Redemption Rule Tenant Category"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'tenant_category_id': fields.many2one('rdm.tenant.category','Tenant Category') 
    }

rdm_rules_tenant_category()

class rdm_rules_bank(osv.osv):
    _name = "rdm.rules.bank"
    _description = "Redemption Rule Bank"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'bank_id': fields.many2one('rdm.bank','Bank')        
    }
    
class rdm_rules_bank_card(osv.osv):
    _name = "rdm.rules.bank.card"
    _description = "Redemption Rule Bank Card"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'bank_card_id': fields.many2one('rdm.bank.card','Bank Card') 
    }

rdm_rules_bank_card()

class rdm_rules_cash(osv.osv):
    _name = "rdm.rules.cash"
    _description = "Redemption Rule Cash"
    _columns = {
        'rules_detail_id': fields.many2one('rdm.rules.detail','Rules ID', readonly=True),
        'bank_id': fields.many2one('rdm.bank','Exclude Bank') 
    }

rdm_rules_cash()

