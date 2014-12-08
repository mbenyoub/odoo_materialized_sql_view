# -*- coding: utf-8 -*-

import psycopg2
import logging
from openerp.osv import osv
from openerp import SUPERUSER_ID

logger = logging.getLogger(__name__)


class AbstractMaterializedSqlView(osv.AbstractModel):
    """
        This class is an abstract model to help developer to create/refresh/update
        materialized view.
    """
    _name = 'abstract.materialized.sql.view'
    _description = u"This is an helper class to manage materialized SQL view"
    _auto = False

    """
        The name of the materialized sql view.
        Must be defined in inherit class (using inherit = [])
    """
    _sql_mat_view_name = ''
    """
        The name of the sql view used to generate the materialized view
        Must be defined in inherit class (using inherit = [])
    """
    _sql_view_name = ''
    """
        The sql query to generate the view (without any create views)
    """
    _sql = ''

    def init(self, cr):
        """
            Init method is called when installing or updating the module.
            As we can't know if the model of the sql changed, we have to drop materialized view
            and recreate it.
        """
        # prevent against Abstract class initialization
        if type(self) == AbstractMaterializedSqlView:
            return

        logger.info(u"Init materialized view, using Postgresql %r",
                    cr._cnx.server_version)
        self.create_views(cr, SUPERUSER_ID)
        # TODO: use postgresql materialized view if version > 9.3

    def safe_properties(self):
        if not self._sql:
            raise osv.except_osv(u"Properties must be defined in subclass",
                                 u"_sql properties should be redifined in sub class"
                                 )
        if not self._sql_mat_view_name:
            self._sql_mat_view_name = self._table
        if not self._sql_view_name:
            self._sql_view_name = self._table + '_view'

    def create_views(self, cr, uid, context=None):
        self.safe_properties()
        logger.info("Create Materialized view %r", self._sql_mat_view_name)
        self.change_matview_state(cr, uid, 'before_create_view', context=context)
        self.drop_views_if_exist(cr, uid, context=context)
        try:
            self.before_create(cr, uid, context=context)
            cr.execute("CREATE VIEW %(view_name)s AS (%(sql)s)" %
                       dict(view_name=self._sql_view_name, sql=self._sql, ))
            cr.execute("CREATE TABLE %(mat_view_name)s AS SELECT * FROM %(view_name)s" %
                       dict(mat_view_name=self._sql_mat_view_name,
                            view_name=self._sql_view_name,
                            ))
            self.after_create(cr, uid, context=context)
        except psycopg2.Error as e:
            self.report_sql_error(cr, uid, e, context=context)
        result = self.change_matview_state(cr, uid, 'after_refresh_view', context=context)
        return result

    def refresh_materialized_view(self, cr, uid, context=None):
        result = []
        self.safe_properties()
        logger.info("Refresh Materialized view %r", self._sql_mat_view_name)
        self.change_matview_state(cr, uid, 'before_refresh_view', context)
        try:
            self.before_refresh(cr, uid, context=context)
            cr.execute("DELETE FROM %(mat_view_name)s" % dict(mat_view_name=self._sql_mat_view_name,
                                                              ))
            cr.execute("INSERT INTO %(mat_view_name)s SELECT * FROM %(view_name)s" %
                       dict(mat_view_name=self._sql_mat_view_name,
                            view_name=self._sql_view_name,
                            ))
            self.after_refresh(cr, uid, context=context)
        except psycopg2.Error as e:
            self.report_sql_error(cr, uid, e, context=context)
        else:
            result = self.change_matview_state(cr, uid, 'after_refresh_view', context=context)
        return result

    def change_matview_state(self, cr, uid, method_name, context=None):
        matview_stat = self.pool.get('materialized.sql.view')
        # Make sure object exist or create it
        matview_stat.create_if_not_exist(cr, uid, {
            'model_name': self._name,
            'view_name': self._sql_view_name,
            'matview_name': self._sql_mat_view_name,
            'pg_version': cr._cnx.server_version}, context=context)
        method = getattr(matview_stat, method_name)
        return method(cr, uid, self._sql_mat_view_name, context=context)

    def drop_views_if_exist(self, cr, uid, context=None):
        self.safe_properties()
        logger.info("Drop Materialized view %r", self._sql_mat_view_name)
        try:
            self.before_drop(cr, uid, context=context)
            cr.execute("DROP TABLE IF EXISTS %s CASCADE" % (self._sql_mat_view_name))
            cr.execute("DROP VIEW IF EXISTS %s CASCADE" % (self._sql_view_name,))
        except psycopg2.Error as e:
            self.report_sql_error(cr, uid, e, context=context)
        return self.change_matview_state(cr, uid, 'after_drop_view', context=context)

    def report_sql_error(self, cr, uid, err, context=None):
        if not context:
            context = {}
        context.update({'error_message': err.pgerror})
        cr.rollback()
        self.change_matview_state(cr, uid, 'aborted_matview', context=context)

    def before_drop(self, cr, uid, context=None):
        """
            Method called before drop materialized view and view,
            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def before_create(self, cr, uid, context=None):
        """
            Method called before create materialized view and view,
            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def after_create(self, cr, uid, context=None):
        """
            Method called after create materialized view and view,
            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def before_refresh(self, cr, uid, context=None):
        """
            Method called before refresh materialized view,
            this was made to do things like drop index before in the same transaction.

            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def after_refresh(self, cr, uid, context=None):
        """
            Method called after refresh materialized view,
            this was made to do things like add index after refresh data

            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def write(self, cr, uid, ids, context=None):
        raise osv.except_osv(u"Write on materialized view is forbidden",
                             u"Write on materialized view is forbidden,"
                             u"because data would be lost at the next refresh"
                             )

    def create(self, cr, uid, ids, context=None):
        raise osv.except_osv(u"Create data on materialized view is forbidden",
                             u"Create data on materialized view is forbidden,"
                             u"because data would be lost at the next refresh"
                             )

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(u"Remove data on materialized view is forbidden",
                             u"Remove data on materialized view is forbidden,"
                             u"because data would be lost at the next refresh"
                             )
