# -*- coding: utf-8 -*-
from anybox.testing.openerp import SharedSetupTransactionCase
from openerp.osv import osv


class AbstractMaterializedSqlViewTester(SharedSetupTransactionCase):

    @classmethod
    def initTestData(self):
        super(AbstractMaterializedSqlViewTester, self).initTestData()
        self.demo_mdl = self.registry('test.materialized.view')
        self.users_mdl = self.registry('res.users')

        self.user_id = self.ref('base.partner_demo')
        self.group_id = self.ref('base.group_user')

    def test_write_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_mdl.write,
                          self.cr, self.uid, [self.group_id], {'name': 'Test'})

    def test_unlink_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_mdl.unlink,
                          self.cr, self.uid, [self.group_id])

    def test_create_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_mdl.unlink,
                          self.cr, self.uid, {'name': 'Test'})

    def test_read_and_refresh_materialized_view(self):
        cr, uid = self.cr, self.uid
        # Get the user_count for group_id
        user_count = self.demo_mdl.read(cr, uid, self.group_id, ['user_count'])['user_count']
        # add user on group_id
        self.users_mdl.create(cr, uid, {'name': u"Test user",
                                        'login': u"ttt",
                                        'company_id': self.ref('base.main_company'),
                                        'customer': False,
                                        'email': 'demo@yourcompany.example.com',
                                        'street': u"Avenue des Dessus-de-Lives, 2",
                                        'city': u"Namue",
                                        'zip': '5101',
                                        'country_id': self.ref('base.be'), })
        # The user count havn't increase until we refresh the view
        self.assertEquals(self.demo_mdl.read(cr, uid, self.group_id, ['user_count'])['user_count'],
                          user_count)
        # Refresh the materialized view
        self.demo_mdl.refresh_materialized_view(cr)
        # Read user count, there is one more now!
        self.assertEquals(self.demo_mdl.read(cr, uid, self.group_id, ['user_count'])['user_count'],
                          user_count)
