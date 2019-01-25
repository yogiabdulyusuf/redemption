from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class rdm_customer(models.Model):
    _inherit = "rdm.customer"
    
    # def get_points(self):
    #     id = self.id
    #     res = {}
    #     total_point = self.env['rdm.customer.point']
    #     _logger.info('Total Point : ' + str(total_point))
    #
    #     if total_point is None:
    #         total_point = 0
    #
    #     res[id] = total_point
    #     return res

    # point = fields.function(get_points, type="integer", string='Points')
    customer_point_ids = fields.One2many(comodel_name="rdm.customer.point", inverse_name="customer_id", string="Points", required=False, )
