from odoo import models, fields, api


class Tag(models.Model):
    _name = 'lp.tag'
    _description = "Tag"
    _order = 'write_date desc'

    type = fields.Selection(OPPORTUNITY_TYPE, 'Type', readonly=True)
    can_be_attached_in_creation_from_contact = fields.Boolean('Can be attached in creation from contact?', default=False, readonly=True)
