=====================
Materialized SQL VIEW
=====================

This odoo module, add utilities to manage materialized SQL view
and necessary user interface to interact with.

* Odoo v7 should used `default` branch
* Odoo v8 should used `8.0` branch

`Check the bot status
<https://buildbot.anybox.fr/waterfall?category=pv-lead&category=pv-lead&category=pv-lead&reload=60>`_,
the code is tested on on our CI bot.

How to use it
-------------

You can have a look to `the basic example
<https://bitbucket.org/anybox/materialized_sql_view/src/default/test_materialized_sql_view/model/model_test_using_sql_mat_view.py>`_,
used in test module: `test_materialized_sql_view`.

You can etheir add cron to refresh the materialized view periodicly, 
`here <https://bitbucket.org/anybox/materialized_sql_view/src/default/test_materialized_sql_view/data/ir_cron.xml>`_ 
an example on the previous model


Features
--------

* UI to manage materialized Sql view, and manually launch refresh
    - add `Materialized sql view Manager` group to your expected user.
    - Go through `Settings > Technical > Database Structure > Materialized SQL view`
      menu to manage materialized sql views
* Abstract class, to help developer to create materialized sql view
* Use postgresql materialized view if pg >= 9.3.0.


TODO
----

* Manage when pg version changed.
* Add helper to avoid recreate materialized sql view if it isn't necessary
   (model not changed and same database version) when updating module
* Add UI on models based on materialized view. Specialy on dashboards


Installation
------------

Nothing specific here,

If you are using the `anybox.recipe.openerp`, add the following line::

     hg https://bitbucket.org/anybox/materialized_sql_view materialized_sql_view default


Else, download the module and add it in the odoo path as any others odoo module.

Support
-------

If you are having issues, please let us know using `Bitbucket issue tracker
<https://bitbucket.org/anybox/materialized_sql_view/issues?status=new&status=open>`_.
