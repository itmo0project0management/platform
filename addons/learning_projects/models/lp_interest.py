from odoo import models, fields, api
from random import randint
from odoo.exceptions import ValidationError

class Interest(models.Model):
    _name = 'lp.interest'
    _description = "Область интересов пользователя"
    _order = 'write_date desc'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Интересы', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)

    @api.constrains('name')
    def _check_duplicate_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 0:
                raise ValidationError("Interest with this name already exists.")