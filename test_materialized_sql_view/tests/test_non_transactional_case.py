from anybox.testing.openerp import TransactionCase


class NonTransactionalCase(TransactionCase):

    def setUp(self):
        super(NonTransactionalCase, self).setUp()
        self.demo_matview_mdl = self.registry('test.materialized.view')
        self.mat_view_mdl = self.registry('materialized.sql.view')
        self.context = {'ascyn': False}

    def test_overload_before_refresh(self):
        save_method = self.demo_matview_mdl.before_refresh_materialized_view

        def before_refresh_materialized_view(cr, uid, context=None):
            cr.execute("test")

        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.before_refresh_materialized_view = before_refresh_materialized_view
        self.demo_matview_mdl.refresh_materialized_view(cr, uid, context=self.context)
        self.demo_matview_mdl.before_refresh_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')

    def test_overload_after_refresh(self):
        save_method = self.demo_matview_mdl.after_refresh_materialized_view

        def after_refresh_materialized_view(cr, uid, context=None):
            cr.execute("test")

        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.after_refresh_materialized_view = after_refresh_materialized_view
        self.demo_matview_mdl.refresh_materialized_view(cr, uid, context=self.context)
        self.demo_matview_mdl.after_refresh_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')

    def test_overload_before_drop(self):
        cr, uid = self.cr, self.uid
        save_method = self.demo_matview_mdl.before_drop_materialized_view

        def before_drop_materialized_view(cr, uid, context=None):
            cr.execute("test")

        self.demo_matview_mdl.before_drop_materialized_view = before_drop_materialized_view
        self.demo_matview_mdl.drop_views_if_exist(cr, uid, context=self.context)
        self.demo_matview_mdl.before_drop_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')
        self.demo_matview_mdl.create_views(cr, uid, context=self.context)

    def test_overload_after_drop(self):
        save_method = self.demo_matview_mdl.after_drop_materialized_view

        def after_drop_materialized_view(cr, uid, context=None):
            cr.execute("test")

        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.after_drop_materialized_view = after_drop_materialized_view
        self.demo_matview_mdl.drop_views_if_exist(cr, uid, context=self.context)
        self.demo_matview_mdl.after_drop_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')
        self.demo_matview_mdl.create_views(cr, uid, context=self.context)

    def test_overload_before_create(self):
        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.drop_views_if_exist(cr, uid, context=self.context)
        save_method = self.demo_matview_mdl.before_create_materialized_view

        def before_create_materialized_view(cr, uid, context=None):
            cr.execute("test")

        self.demo_matview_mdl.before_create_materialized_view = before_create_materialized_view
        self.demo_matview_mdl.create_views(cr, uid, context=self.context)
        self.demo_matview_mdl.before_create_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')

    def test_overload_after_create(self):
        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.drop_views_if_exist(cr, uid, context=self.context)
        save_method = self.demo_matview_mdl.after_create_materialized_view

        def after_create_materialized_view(cr, uid, context=None):
            cr.execute("test")

        self.demo_matview_mdl.after_create_materialized_view = after_create_materialized_view
        self.demo_matview_mdl.create_views(cr, uid, context=self.context)
        self.demo_matview_mdl.after_create_materialized_view = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')
