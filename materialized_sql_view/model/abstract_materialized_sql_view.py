# -*- coding: utf-8 -*-

import logging
from openerp.osv import osv
# from openerp import SUPERUSER_ID

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
                    cr._cnx.get_parameter_status('server_version'))
        self.create_views(cr)
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

    def create_views(self, cr):
        self.safe_properties()
        self.drop_views_if_exist(cr)
        cr.execute("CREATE VIEW %(view_name)s AS (%(sql)s)" % dict(view_name=self._sql_view_name,
                                                                   sql=self._sql,
                                                                   ))
        cr.execute("CREATE TABLE %(mat_view_name)s AS SELECT * FROM %(view_name)s" %
                   dict(mat_view_name=self._sql_mat_view_name,
                        view_name=self._sql_view_name,
                        ))
        self.after_create(cr)

    def refresh_materialized_view(self, cr):
        self.safe_properties()
        self.before_refresh(cr)
        cr.execute("DELETE FROM %(mat_view_name)s" % dict(mat_view_name=self._sql_mat_view_name,
                                                          ))
        cr.execute("INSERT INTO %(mat_view_name)s SELECT * FROM %(view_name)s" %
                   dict(mat_view_name=self._sql_mat_view_name,
                        view_name=self._sql_view_name,
                        ))
        self.after_refresh(cr)

    def drop_views_if_exist(self, cr):
        self.safe_properties()
        self.before_drop(cr)
        cr.execute("DROP TABLE IF EXISTS %s CASCADE" % (self._sql_mat_view_name))
        cr.execute("DROP VIEW IF EXISTS %s CASCADE" % (self._sql_view_name,))

    def before_drop(self, cr):
        """
            Method called before drop materialized view and view,
            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def after_create(self, cr):
        """
            Method called after create materialized view and view,
            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def before_refresh(self, cr):
        """
            Method called before refresh materialized view,
            this was made to do things like drop index before in the same transaction.

            Nothing done in abstract method, it's  hook to used in subclass
        """
        pass

    def after_refresh(self, cr):
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
