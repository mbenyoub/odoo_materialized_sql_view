# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

TABLE_NAME = 'test_materialized_view'


class ModelTestUsingSqlMatView(osv.Model):
    """This model is only used to test materialized_sql_view module.
       As an example we will calulate the number of res.users per res.groups
    """
    _name = 'test.materialized.view'
    _description = u"Model used to test the module"
    _table = TABLE_NAME

    _inherit = [
        'abstract.materialized.sql.view',
    ]

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'group_id': fields.many2one('res.groups', u"Group"),
        'user_count': fields.integer('Users count')
    }

    _sql_mat_view_name = TABLE_NAME
    _sql_view_name = TABLE_NAME + '_view'
    _sql = """SELECT g.id, g.name, g.id as group_id, count(*) as user_count
              FROM res_groups g
                    INNER JOIN res_groups_users_rel rel ON g.id = rel.gid
                    INNER JOIN res_users u ON rel.uid = u.id
              GROUP BY g.id, g.name, g.id
           """
