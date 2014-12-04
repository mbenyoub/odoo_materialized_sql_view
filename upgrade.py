# -*- python -*-
"""This is a template upgrade script.

The purpose is both to cover the most common use-case (updating all modules)
and to provide an example of how this works.
"""


def run(session, logger):
    """Update all modules."""
    if session.is_initialization:
        logger.info("Install materialized_sql_view modules.")
        session.install_modules(['materialized_sql_view'])
    else:
        logger.info("updating materialized_sql_view modules.")
        session.update_modules(['materialized_sql_view'])
