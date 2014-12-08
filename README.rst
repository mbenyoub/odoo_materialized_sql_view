=====================
Materialized SQL VIEW
=====================

This v7.0 odoo module, add utilities to manage materialized SQL view
and necessary user interface to interact with.

How to use it
-------------

You can have a look to this basic example, used in test module: `test_materialized_sql_view`.

.. literalinclude:: test_materialized_sql_view/model/model_test_using_sql_mat_view.py
   :language: python

If you want to add a cron::

.. literalinclude:: test_materialized_sql_view/data/ir_cron.xml
   :language: xml

Features
--------

 * UI to manage materialized Sql view, and manually launch refresh
    - add user to the `Materialized sql view Manager` group
    - Go through `Settings > Technical > Database Structure > Materialized SQL view` menu
 * Abstract class, to help developer to create materialized sql view


TODO
----

 * Add helper to avoid recreate materialized sql view if it isn't necessary
   (model not changed and same database version) when updating module
 * Use postgresql materialized view if pg >= 9.3.0. And well manage when pg version changed.
 * Add UI on models based on materialized view. Specialy on dashboards


Installation
------------

Nothing specific here,

If you are using the `anybox.recipe.odoo`, add the following line::

     hg https://bitbucket.org/anybox/materialized_sql_view materialized_sql_view default


Else, download the module, add it in the odoo path as any odoo module.

Support
-------

If you are having issues, please let us know using `Bitbucket issue tracker
<https://bitbucket.org/anybox/materialized_sql_view/issues?status=new&status=open>`_.
