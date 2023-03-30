from odoo import models, fields
from random import randint


class Interest(models.Model):
    _name = 'lp.interest'
    _description = "Область интересов пользователя"
    _order = 'write_date desc'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Интересы', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)
