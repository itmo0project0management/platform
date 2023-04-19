import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

ACADEMIC_DEGREE = [
    ("bachelor", 'Бакалавр'),
    ("master", 'Магистрант'),
    ("aspirant", 'Аспирант'),
]

FULL_FIO_TEMPLATE = "{last_name} {name} {surname}"


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = "Partner"
    _order = 'write_date desc'

    name = fields.Char(string='ФИО', tracking=True)
    firstname = fields.Char(string='Firstname', tracking=True)
    lastname = fields.Char(string='Lastname', tracking=True)

    academic_degree = fields.Selection(ACADEMIC_DEGREE, "Академическая степень", readonly=True)
    in_project = fields.Boolean("В проекте", readonly=True, tracking=True)
    ear = fields.Char("Год", tracking=True)
    number_groups = fields.Char("Группа", readonly=True ,tracking=True)
    category_id = fields.Many2many('res.partner.category', string='Skill Stack', tracking=True)

    @api.model
    def create(self, vals):
        return super(Partner, self).create(vals)

    def write(self, vals):
        return super(Partner, self).write(vals)
