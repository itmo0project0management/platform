import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProjectInvitations(models.Model):
    _name = 'lp.project.invitations'
    _description = 'Projects Invitations'

    # invitations = fields.Many2Many('lp.invitation', string="invitations", limit=2)
