import time

from openerp.report import report_sxw
from openerp import pooler


class rdm_reward_trans_list_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(rdm_reward_trans_list_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.rdm.reward.trans.list.webkit',
                      'rdm.reward.trans',
                      'jakcaddons/jakc_redemption_reward_webkit_report/report/redemption_reward_trans_list.mako',
                      parser=rdm_reward_trans_list_report)
    