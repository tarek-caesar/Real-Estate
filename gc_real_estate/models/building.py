# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GcBuilding(models.Model):
    _name = 'gc.building'
    _rec_name = 'name'
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Building name already exists')]

    name = fields.Char(string='Name', help="Building Name", required=True)
    rental_area = fields.Float(
        compute="_compute_total_area",
        string='Rental Area',
        help="Rental Area",
    )
    apartment = fields.One2many(
        'gc.apartment',
        'building',
        string='Apartments'
    )
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one(
        "res.country.state",
        string='State',
        domain="[('country_id', '=', country_id)]"
    )
    country_id = fields.Many2one('res.country', string='Country')

    @api.depends('apartment')
    def _compute_total_area(self):
        """
        Compute total area of the building by summing apartment areas for
        this building.
        """
        for rec in self:
            rec.rental_area = sum([apr.area for apr in rec.apartment])

    @api.multi
    def write(self, vals):
        """
        This implementation insures that if building name is changed then
        apartment names should be updated as well (keeping the same
        sequence as is).
        :param vals: dictionary with updated values
        :return: updated gc.building record
        """
        if vals.get('name', False):
            for rec in self:
                for apartment in rec.apartment:
                    old_apartment_name_splitted = apartment.name.split('_')
                    apartment.write({
                        'name': vals['name']
                        + '_' + old_apartment_name_splitted[1]
                    })
        res = super(GcBuilding, self).write(vals)
        return res
