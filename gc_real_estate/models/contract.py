# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GcContract(models.Model):
    _name = 'gc.contract'
    _rec_name = 'tenant'

    tenant = fields.Many2one(
        'res.partner',
        string='Tenant',
        help="Partner or Client",
        required=True
    )
    building = fields.Many2one(
        'gc.building',
        string='Building',
        help="Related Building",
        required=True
    )
    apartment = fields.Many2one(
        'gc.apartment',
        string='Apartment',
        help="Related Apartment",
        domain="[('rented', '=', False)]"
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        help="Contract Start Date"
    )
    end_date = fields.Date(
        string='End Date',
        help="Contract End Date"
    )

    @api.onchange('building')
    def filter_apartments(self):
        if self.building:
            apartments = self.env['gc.apartment'].\
                search([
                    ('building', '=', self.building.id),
                    ('rented', '=', False)
                ])
            apartments_list = list()
            for apartment in apartments:
                apartments_list.append(apartment.id)
            res = dict()
            res['domain'] = {'apartment': [('id', 'in', apartments_list)]}
            return res
