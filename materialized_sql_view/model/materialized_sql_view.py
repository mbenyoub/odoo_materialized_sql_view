# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime
from openerp import SUPERUSER_ID

MATERIALIZED_SQL_VIEW_STATES = [('nonexistent', 'Nonexistent'),
                                ('creating', 'Creating'),
                                ('pendingrefresh', 'Pending Refresh'),
                                ('refreshing', 'Refreshing'),
                                ('refreshed', 'Refreshed'),
                                ('error', 'Error'),
                                ]


class MaterializedSqlView(osv.Model):
    _name = 'materialized.sql.view'
    _description = u"Materialized SQL View"

    _columns = {
        'name': fields.char('Name', required=True),
        'model_id': fields.many2one('ir.model', 'Model', required=True, delete='cascade'),
        'view_name': fields.char('SQL view name', required=True, readonly=True),
        'matview_name': fields.char('Materialized SQL View Name', required=True, readonly=True),
        'last_refresh_start_date': fields.datetime('Last refreshed start date', readonly=True),
        'last_refresh_end_date': fields.datetime('Last refreshed end date', readonly=True),
        'state': fields.selection(MATERIALIZED_SQL_VIEW_STATES, 'State', required=True,
                                  readonly=True)
    }

    _defaults = {
        'state': 'nonexistent',
    }

    def launch_refresh_materialized_sql_view(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        if context.get('ascyn', False):
            self.schedul_refresh_materialized_sql_view(cr, uid, ids, context)
            return self.write(cr, uid, ids, {'state': 'pendingrefresh'}, context=context)
        else:
            return self.refresh_materialized_view(cr, uid, ids, context)

    def schedul_refresh_materialized_sql_view(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        uid = context.get('delegate_user', uid)
        vals = {
            'name': u"Refresh materialized views",
            'user_id': uid,
            'priority': 100,
            'numbercall': 1,
            'doall': True,
            'model': self._name,
            'function': 'refresh_materialized_view',
            'args': repr((ids, context)),
        }
        # use super user id because ir.cron have not to be accessible to normal user
        self.pool.get('ir.cron').create(cr, SUPERUSER_ID, vals, context=context)

    def refresh_materialized_view(self, cr, uid, ids, context=None):
        result = []
        if not context:
            context = {}
        self.pool.get('')
        uid = context.get('user_id', uid)
        matviews_performed = []
        ir_model = self.pool.get('ir.model')
        for matview in self.read(cr, uid, ids, ['id', 'model_id', 'matview_name'], context=context,
                                 load='_classic_write'):
            if matview['matview_name'] in matviews_performed:
                continue
            self.before_refresh_view(cr, uid, matview['matview_name'], context)
            if not context.get('unittest', False):
                cr.commit()
            model = ir_model.read(cr, uid, matview['model_id'], ['model'], context)['model']
            matview_mdl = self.pool.get(model)
            matview_mdl.refresh_materialized_view(cr)
            result.append(self.after_refresh_view(cr, uid, matview['matview_name'], context))
            if not context.get('unittest', False):
                cr.commit()
            matviews_performed.append(matview['matview_name'])
        return result

    def search_materialized_sql_view_ids_from_matview_name(
            self, cr, uid, matview_name, context=None):
        return self.search(cr, uid, [('matview_name', '=', matview_name)], context=context)

    def before_refresh_view(self, cr, uid, matview_name, context=None):
        ids = self.search_materialized_sql_view_ids_from_matview_name(cr, uid, matview_name,
                                                                      context=context)
        return self.write(cr, uid, ids, {'last_refresh_start_date': datetime.now(),
                                         'state': 'refreshing'})

    def after_refresh_view(self, cr, uid, matview_name, context=None):
        ids = self.search_materialized_sql_view_ids_from_matview_name(cr, uid, matview_name,
                                                                      context=context)
        return self.write(cr, uid, ids, {'last_refresh_end_date': datetime.now(),
                                         'state': 'refreshed'})
