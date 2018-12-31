import time

from openerp.report import report_sxw
from openerp import pooler


class rdm_trans_list_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(rdm_trans_list_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.rdm.trans.list.webkit',
                      'rdm.trans',
                      'jakcaddons/jakc_redemption_trans_webkit_report/report/redemption_trans_list.mako',
                      parser=rdm_trans_list_report)


class rdm_trans_detail_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(rdm_trans_detail_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.rdm.trans.detail.webkit',
                      'rdm.trans',
                      'jakcaddons/jakc_redemption_trans_webkit_report/report/redemption_trans_detail.mako',
                      parser=rdm_trans_detail_report)
    