# -*- coding: utf-8 -*-
from anybox.testing.openerp import SharedSetupTransactionCase
from datetime import datetime


class MaterializedSqlView(SharedSetupTransactionCase):

    @classmethod
    def initTestData(self):
        super(MaterializedSqlView, self).initTestData()
        self.matview_mdl = self.registry('materialized.sql.view')
        self.demo_matview_mdl = self.registry('test.materialized.view')
        self.users_mdl = self.registry('res.users')

        self.context = {'unittest': True, 'ascyn': False}
        mdl_id = self.registry('ir.model').search(
            self.cr, self.uid, [('model', '=', self.demo_matview_mdl._name)])[0]
        values = {'name': u"Model test",
                  'model_id': mdl_id,
                  'view_name': self.demo_matview_mdl._sql_view_name,
                  'matview_name': self.demo_matview_mdl._sql_mat_view_name,
                  'state': 'nonexistent'
                  }
        self.matview_id = self.matview_mdl.create(self.cr, self.uid, values, context=self.context)

    def test_simple_case(self):
        """Test some simple case, create/read/write/unlink"""
        users_mdl_id = self.registry('ir.model').search(self.cr, self.uid,
                                                        [('model', '=', 'res.users')],
                                                        context=self.context)[0]
        values = {'name': u"Test",
                  'model_id': users_mdl_id,
                  'view_name': u'test_view',
                  'matview_name': u'test_mat_viewname',
                  'last_refresh_start_date': datetime.now(),
                  'last_refresh_end_date': datetime.now(),
                  }
        id = self.matview_mdl.create(self.cr, self.uid, values)
        self.matview_mdl.write(self.cr, self.uid, [id], {'name': u"Fake test"},
                               context=self.context)
        values.update({'name': u"Fake test",
                       'state': u'nonexistent',
                       })
        # don't wan't to get headheak to fix format date here
        values.pop('last_refresh_start_date')
        values.pop('last_refresh_end_date')
        self.assertRecord(self.matview_mdl, id, values)
        self.matview_mdl.unlink(self.cr, self.uid, [id], context=self.context)

    def test_search_materialized_sql_view_ids_from_matview_name(self):
        self.assertTrue(
            self.matview_id in
            self.matview_mdl.search_materialized_sql_view_ids_from_matview_name(
                self.cr, self.uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context))

    def test_launch_refresh_materialized_sql_view(self):
        cr, uid = self.cr, self.uid
        group_id = self.ref('base.group_user')

        user_count = self.demo_matview_mdl.read(cr, uid, group_id, ['user_count'])['user_count']
        self.users_mdl.create(cr, uid, {'name': u"Test user",
                                        'login': u"ttt",
                                        'company_id': self.ref('base.main_company'),
                                        'customer': False,
                                        'email': 'demo@yourcompany.example.com',
                                        'street': u"Avenue des Dessus-de-Lives, 2",
                                        'city': u"Namue",
                                        'zip': '5101',
                                        'country_id': self.ref('base.be'), }, context=self.context)
        self.assertEquals(
            self.demo_matview_mdl.read(cr, uid, group_id, ['user_count'],
                                       context=self.context)['user_count'],
            user_count)
        ids = self.matview_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name)
        self.matview_mdl.launch_refresh_materialized_sql_view(cr, uid, ids, context=self.context)
        for rec in self.matview_mdl.read(cr, uid, ids, ['state'], context=self.context):
            self.assertEquals(rec['state'], 'refreshed')
        # Read user count, there is one more now!
        self.assertEquals(
            self.demo_matview_mdl.read(cr, uid, group_id, ['user_count'],
                                       context=self.context)['user_count'],
            user_count + 1)

    def test_before_refresh_view(self):
        self.matview_mdl.before_refresh_view(
            self.cr, self.uid, self.demo_matview_mdl._sql_mat_view_name)
        self.assertEquals(self.matview_mdl.read(
            self.cr, self.uid, [self.matview_id], ['state'], context=self.context)[0]['state'],
            'refreshing')

    def test_after_refresh_view(self):
        self.matview_mdl.after_refresh_view(
            self.cr, self.uid, self.demo_matview_mdl._sql_mat_view_name)
        self.assertEquals(self.matview_mdl.read(
            self.cr, self.uid, [self.matview_id], ['state'], context=self.context)[0]['state'],
            'refreshed')
