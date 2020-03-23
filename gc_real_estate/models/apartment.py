# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GcApartment(models.Model):
    _name = 'gc.apartment'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        help="Apartment Name",
        default=lambda self: _('New')
    )
    building = fields.Many2one(
        'gc.building',
        string='Building',
        help="Related Building",
        required=True
    )
    area = fields.Float(
        string='Apartment Area',
        help="Apartment Area (Should be greater than 0)",
    )

    rented = fields.Boolean(
        string='Rented',
        compute='_compute_is_rented',
        help="Indicate whether this apartment is rented or not",
        store=True
    )
    contracts = fields.One2many(
        'gc.contract',
        'apartment',
        string="Contracts",
        help="This additional field is used to trigger "
             "_compute_is_rented function since the field (rented) "
             "is stored."
    )

    @api.multi
    @api.depends('contracts.start_date', 'contracts.end_date')
    def _compute_is_rented(self):
        """
        Check if the apartment is rented based on contract period.
        """
        for rec in self:
            contract = self.env['gc.contract'] \
                .search([('apartment.id', '=', rec.id)])
            start_date = fields.Date.from_string(contract.start_date) \
                or False
            end_date = fields.Date.from_string(contract.end_date) \
                or False
            current_date = fields.Date.from_string(fields.Date.today())
            available = False
            if start_date:
                if end_date:
                    if start_date <= current_date <= end_date:
                        available = True
                else:
                    if current_date >= start_date:
                        available = True
            if available:
                rec.rented = True
            else:
                rec.rented = False

    @api.model
    def create(self, vals):
        """
        The field name is auto-generated as [building_name]_[index]
        Example: BERBuilding_001, considering that building’s name is
        “BERBuilding”.
        Index starts from 001 on every building.
        :param vals: dictionary of values for apartment record to be
                created.
        :return: apartment record
        """
        if vals.get('name', _('New')) == _('New'):
            building = self.env['gc.building'].browse(vals['building'])
            vals['name'] = building.name + self.env['ir.sequence'].\
                next_by_code('gc.apartment') or _('New')
        result = super(GcApartment, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        """
        Changing apartment building should be prevented.
        :param vals: dictionary of values for apartment record to be
                updated.
        :return: apartment record
        """
        for rec in self:
            if vals.get('building', False) and \
                    vals.get('building', False) != rec.building.id:
                raise ValidationError(_('You cannot move any apartment '
                                        'to another building !'))

        return super(GcApartment, self).write(vals)
