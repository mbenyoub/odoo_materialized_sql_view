from anybox.testing.openerp import TransactionCase


class NonTransactionalCase(TransactionCase):

    def setUp(self):
        super(NonTransactionalCase, self).setUp()
        self.demo_matview_mdl = self.registry('test.materialized.view')
        self.mat_view_mdl = self.registry('materialized.sql.view')
        self.context = {'ascyn': False}

    def test_overload_before_refresh(self):
        save_method = self.demo_matview_mdl.after_refresh

        def after_refresh(cr, uid, context=None):
            cr.execute("test")

        cr, uid = self.cr, self.uid
        self.demo_matview_mdl.after_refresh = after_refresh
        self.demo_matview_mdl.refresh_materialized_view(cr, uid, context=self.context)
        self.demo_matview_mdl.after_refresh = save_method
        ids = self.mat_view_mdl.search_materialized_sql_view_ids_from_matview_name(
            cr, uid, self.demo_matview_mdl._sql_mat_view_name, context=self.context)
        self.assertEqual(
            self.mat_view_mdl.read(
                cr, uid, ids, ['state'], context=self.context)[0]['state'],
            u'aborted')
