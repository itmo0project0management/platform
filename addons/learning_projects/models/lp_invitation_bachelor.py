from odoo import models, fields, api
from odoo.exceptions import ValidationError

STATUS = [
    ("waiting", "В ожидании"),
    ("invited", "Приглашен"),
    ("invited_for_other_priority", "Приглашен по дгугому приоритету"),
]


class InvitationBachelor(models.Model):
    _name = 'lp.invitation.bachelor'
    _description = 'Invitation Bachelor'
    _inherit = ['mail.thread']
    _order = 'priority asc'

    def _domain_project_id(self):
        invitation = self.env['lp.invitation.bachelor'].search([('create_uid', '=', self.env.uid)], limit=1)
        if invitation is None:
            return {}
        return [('id', '!=', invitation.project_id.id)]

    # bachelor
    priority = fields.Integer(string="Приоритет", default=1, size=2, required=True)
    project_id = fields.Many2one('lp.project', string="Проект", required=True, domain=_domain_project_id)
    resume = fields.Many2one('lp.resume', string="Resume", required=True)  # compute='_compute_resume',
    resume_author = fields.Many2one(related='resume.author', string="Отправитель", store=True, readonly=True)
    number_grops = fields.Char(related='resume_author.number_grops', string="Группа", readonly=True)

    invited_by = fields.Many2one('res.partner', string="Приглашён кем", readonly=True, tracking=True)
    invited_status = fields.Selection(STATUS, string="STATUS", default="waiting", readonly=True, tracking=True)

    # Team
    message_partner_ids = fields.Many2many(related='project_id.project.message_partner_ids', string="message_follower_ids", readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        self.validate_count_creations()
        return super(InvitationBachelor, self).create(vals)

    def write(self, vals):
        self.change_priority(vals.get("priority"))
        return super(InvitationBachelor, self).write(vals)

    @api.depends('resume')
    def _compute_resume(self):
        for rec in self:
            resume = self.env['lp.resume'].search([('create_uid', '=', rec.create_uid.id)])
            rec.resume = resume.id

    @api.constrains('priority')
    def _check_priority(self):
        priority = self.priority
        if priority != 1 and priority != 2:
            raise ValidationError('Priority 1 or 2 ' + str(priority))

    def change_priority(self, priority):
        invitation = self.env['lp.invitation.bachelor'].search([('create_uid', '=', self.env.uid)], limit=1)
        if invitation is not None:
            if priority == 1 and invitation.priority != 2:
                invitation.write({'priority': 2})
            elif priority == 2 and invitation.priority != 1:
                invitation.write({'priority': 1})

    def validate_count_creations(self):
        invitations = self.env['lp.invitation.bachelor'].search([('create_uid', '=', self.env.uid)])
        if len(invitations) > 1:
            raise ValidationError("Бакалавр может создать только 2 приглашения")

    def action_confirm_invitation(self):
        resume_author = self.resume_author.id
        lp_p = self.project_id
        if lp_p.is_all_invited:
            raise ValidationError('Вы уже пригласили {max_col_users}'.format(max_col_users=lp_p.max_col_users))

        lp_p.project.message_subscribe(partner_ids=[self.resume_author.id])
        new_current_value_users = lp_p.current_value_users + 1
        lp_p.write({'current_value_users': new_current_value_users})

        self.write({
            'invited_status': 'invited',
            'message_partner_ids': [(4, resume_author)],
            'invited_by': self.env.uid,
        })

        invitation = self.env['lp.invitation.bachelor'].search([('resume_author', '=', resume_author), ('id', '!=', self.id)], limit=1)
        if invitation is not None:
            invitation.write({'invited_status': 'invited_for_other_priority'})


    def name_get(self):
        result = []
        for record in self:
            result.append((record['id'], record.resume.name))
        return result