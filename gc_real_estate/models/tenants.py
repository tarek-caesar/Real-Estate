# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GcTenants(models.Model):
    _inherit = 'res.partner'

    contracts_ids = fields.One2many(
        'gc.contract',
        'tenant',
        string='Contracts'
    )

    is_tenant = fields.Boolean(
        string='Is Tenant',
        compute='_check_is_tenant',
        help="Indicate whether this partner is tenant.",
        store=True
    )

    @api.depends('contracts_ids')
    def _check_is_tenant(self):
        for rec in self:
            if len(rec.contracts_ids) > 0:
                rec.is_tenant = True
            else:
                rec.is_tenant = False

