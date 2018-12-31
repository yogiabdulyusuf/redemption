import time

from openerp.report import report_sxw
from openerp import pooler


class rdm_schemas_detail_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(rdm_schemas_detail_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.rdm.schemas.detail.webkit',
                      'rdm.schemas',
                      'jakcaddons/jakc_redemption_schemas_webkit_report/report/redemption_schemas_detail.mako',
                      parser=rdm_schemas_detail_report)

class rdm_schemas_list_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(rdm_schemas_list_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.rdm.schemas.list.webkit',
                      'rdm.schemas',
                      'jakca1ddons/jakc_redemption_schemas_webkit_report/report/redemption_schemas_list.mako',
                      parser=rdm_schemas_list_report)
    