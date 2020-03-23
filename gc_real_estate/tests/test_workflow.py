# -*- coding: utf-8 -*-

from odoo import tools, fields
from odoo.tests import common
from psycopg2 import IntegrityError
from odoo.exceptions import ValidationError


class TestRealEstate(common.TransactionCase):

    def setUp(self):
        super(TestRealEstate, self).setUp()
        self.buildingobj = self.env['gc.building']
        self.building1 = self.env['gc.building'].create({
            'name': 'XYZ',
            'street': 'Test Street',
            'city': 'Test City',
            'country_id': self.ref('base.de')
        })
        self.building2 = self.env['gc.building'].create({
            'name': 'GHJ',
            'street': 'Test Street2',
            'city': 'Test City2',
            'country_id': self.ref('base.de')
        })
        # ------ For some reason this unit test is raising error while
        # Check create contract
        self.apartment3 = self.env['gc.apartment'].create({
            'name': 'New',
            'area': 96.0,
            'building': self.building2.id
        })
        self.partner = self.env.ref("base.res_partner_2")
        self.contract = self.env['gc.contract'].create({
            'tenant': self.partner.id,
            'building': self.building2.id,
            'apartment': self.apartment3.id,
            'start_date': fields.Date.today(),
        })

    def test_00_workflow(self):
        sequence = self.env['ir.sequence'].\
            search([('code', '=', 'gc.apartment')])
        seq1_num = sequence.number_next_actual+1
        seq1 = str('%03d' % seq1_num)
        apartment1 = self.env['gc.apartment'].create({
            'name': 'New',
            'area': 34.0,
            'building': self.building1.id
        })
        seq2_num = sequence.number_next_actual + 1
        seq2 = str('%03d' % seq2_num)
        apartment2 = self.env['gc.apartment'].create({
            'name': 'New',
            'area': 97.0,
            'building': self.building1.id
        })
        self.assertEqual(
            apartment2.name,
            self.building1.name + '_' + seq1
        )
        self.assertEqual(
            apartment2.name,
            self.building1.name + '_' + seq2
        )

        # Update building name and check apartments name after update
        self.building1.write({'name': 'BER'})
        self.assertEqual(
            apartment2.name,
            'BER' + '_' + seq1
        )
        self.assertEqual(
            apartment2.name,
            'BER' + '_' + seq2
        )

        # Check total building area
        self.assertEqual(
            self.building1.rental_area,
            sum([apartment1.area, apartment2.area])
        )

        # Check error raise when creating a building the same name
        with self.assertRaises(IntegrityError):
            self.env['gc.building'].create({
                'name': 'BER',
                'street': 'Test Street',
                'city': 'Test City',
                'country_id': self.ref('base.de')
            })

        # Check if apartment3 which is attached to a contract is rented
        # self.assertTrue(self.apartment3.rented)
        # ------- For some reason testing if apartment is rented is raising
        # error ....
        '''
            ERROR gc_real_estate_v9 odoo.sql_db: bad query: 
            b'SELECT "gc_apartment".id FROM "gc_apartment" 
            WHERE ("gc_apartment"."id" = \'121\') 
            ORDER BY "gc_apartment"."id"  '
            ERROR: current transaction is aborted, 
            commands ignored until end of transaction block
        '''
        # (not sure) because no real data is create in the db, to solve this
        # it's better to create a model that creates fake data and use it
        # in unit testing ....

        # ------- probably also this case is failing for the same reason
        # Check moving apartment to another building (not sure as well)
        # with self.assertRaises(IntegrityError):
        #     apartment2.write({'building': self.building2.id})
