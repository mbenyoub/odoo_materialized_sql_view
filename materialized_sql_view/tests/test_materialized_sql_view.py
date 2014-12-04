# -*- coding: utf-8 -*-
from anybox.testing.openerp import SharedSetupTransactionCase
from datetime import datetime


class MaterializedSqlView(SharedSetupTransactionCase):

    @classmethod
    def initTestData(self):
        super(MaterializedSqlView, self).initTestData()
        self.matview_mdl = self.registry('materialized.sql.view')

    def test_simple_case(self):
        """Test some simple case, create/read/write/unlink"""
        users_mdl_id = self.registry('ir.model').search(self.cr, self.uid,
                                                        [('model', '=', 'res.users')])[0]
        values = {'name': u"Test",
                  'model_id': users_mdl_id,
                  'view_name': u'test_view',
                  'matview_name': u'test_mat_viewname',
                  'last_refresh_start_date': datetime.now(),
                  'last_refresh_end_date': datetime.now(),
                  }
        id = self.matview_mdl.create(self.cr, self.uid, values)
        self.matview_mdl.write(self.cr, self.uid, [id], {'name': u"Fake test"})
        values.update({'name': u"Fake test",
                       'state': u'nonexistent',
                       })
        # don't wan't to get headheak to fix format date here
        values.pop('last_refresh_start_date')
        values.pop('last_refresh_end_date')
        self.assertRecord(self.matview_mdl, id, values)
        self.matview_mdl.unlink(self.cr, self.uid, [id])
