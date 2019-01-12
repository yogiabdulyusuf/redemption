from odoo import api, fields, models
import logging
from psycopg2.extras import _logging

_logger = logging.getLogger(__name__)

class rdm_schemas(models.Model):
    _name = "rdm.schemas"
    _inherit = "rdm.schemas"
    
    def trans_generate_draw_detail(self):
        _logging.info("Start Generate Draw Detail")
        trans = self.id
        if trans:
            _logging.info("Transaction Found")
            draw_ids = trans.draw_ids            
            for draw_id in draw_ids:                
                for i in range(0, draw_id.quantity):                    
                    values = {}
                    values.update({'draw_id':draw_id.id})
                    values.update({'schemas_id': ids[0]})
                    values.update({'sequence': i + 1})
                    result_id = self.pool.get('rdm.draw.detail').create(cr, uid, values, context=context)
        else:
            _logging.info("Transaction not found")
        _logging.info("End Generate Draw Detail")
        return True
    
    def trans_clear_draw_detail(self):
        _logging.info("Start Clear Draw Detail")
        args = [('schemas_id','=',self.id)]
        detail_ids = self.pool.get('rdm.draw.detail').search(cr, uid, args, context=context)
        self.pool.get('rdm.draw.detail').unlink(cr, uid, detail_ids, context=context)
        _logging.info("End Clear Draw Detail")
        return True


    draw_ids = fields.one2many('rdm.draw','schemas_id', 'Draws')
    draw_detail_ids = fields.one2many('rdm.draw.detail','schemas_id','Draw Detail')
