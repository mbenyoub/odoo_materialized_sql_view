# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

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
        return self.write(cr, uid, ids, {'state': 'refreshing'}, context=context)
