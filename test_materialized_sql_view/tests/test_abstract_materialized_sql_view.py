# -*- coding: utf-8 -*-
from anybox.testing.openerp import SharedSetupTransactionCase
from openerp.osv import osv
from openerp import SUPERUSER_ID


class AbstractMaterializedSqlViewTester(SharedSetupTransactionCase):

    @classmethod
    def initTestData(self):
        super(AbstractMaterializedSqlViewTester, self).initTestData()
        self.demo_matview_mdl = self.registry('test.materialized.view')
        self.mat_view_mdl = self.registry('materialized.sql.view')
        self.users_mdl = self.registry('res.users')

        self.context = {'ascyn': False}
        self.user_id = self.ref('base.partner_demo')
        self.group_id = self.ref('base.group_user')

    def test_write_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_matview_mdl.write,
                          self.cr, self.uid, [self.group_id], {'name': 'Test'})

    def test_unlink_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_matview_mdl.unlink,
                          self.cr, self.uid, [self.group_id], context=self.context)

    def test_create_forbidden(self):
        self.assertRaises(osv.except_osv,
                          self.demo_matview_mdl.unlink,
                          self.cr, self.uid, {'name': 'Test'}, context=self.context)

    def test_read_and_refresh_materialized_view(self):
        cr, uid = self.cr, self.uid
        # Get the user_count for group_id
        user_count = self.demo_matview_mdl.read(cr, uid, self.group_id, ['user_count'],
                                                context=self.context)['user_count']
        # add user on group_id
        self.users_mdl.create(cr, uid, {'name': u"Test user",
                                        'login': u"ttt",
                                        'company_id': self.ref('base.main_company'),
                                        'customer': False,
                                        'email': 'demo@yourcompany.example.com',
                                        'street': u"Avenue des Dessus-de-Lives, 2",
                                        'city': u"Namue",
                                        'zip': '5101',
                                        'country_id': self.ref('base.be'), }, context=self.context)
        # The user count havn't increase until we refresh the view
        self.assertEquals(self.demo_matview_mdl.read(cr, uid, self.group_id, ['user_count'],
                                                     context=self.context)['user_count'],
                          user_count)
        # Refresh the materialized view
        self.demo_matview_mdl.refresh_materialized_view(cr, SUPERUSER_ID, context=self.context)
        # Read user count, there is one more now!
        self.assertEquals(self.demo_matview_mdl.read(cr, uid, self.group_id, ['user_count'],
                                                     context=self.context)['user_count'],
                          user_count + 1)

    def test_safe_properties(self):
        self.demo_matview_mdl._sql_mat_view_name = ''
        self.demo_matview_mdl._sql_view_name = ''
        self.demo_matview_mdl.safe_properties()
        self.assertEquals(self.demo_matview_mdl._sql_mat_view_name, self.demo_matview_mdl._table)
        self.assertEquals(self.demo_matview_mdl._sql_view_name,
                          self.demo_matview_mdl._table + '_view')
        sql = self.demo_matview_mdl._sql
        self.demo_matview_mdl._sql = ''
        self.assertRaises(osv.except_osv,
                          self.demo_matview_mdl.safe_properties
                          )
        # Set it back to iniatial value, this is used in some other unit test
        self.demo_matview_mdl._sql = sql

    def test_change_matview_state(self):
        self.demo_matview_mdl.change_matview_state(self.cr, self.uid,
                                                   'after_refresh_view',
                                                   context=self.context)
        self.assertRaises(AttributeError,
                          self.demo_matview_mdl.change_matview_state, self.cr, self.uid, 'test')
