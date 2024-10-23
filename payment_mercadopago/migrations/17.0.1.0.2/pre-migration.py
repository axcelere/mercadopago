from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """
    The objective of this is delete the original view form the module how bring the functionality
    adding in the previous commit
    """
    openupgrade.logged_query(
        env.cr,
        """UPDATE ir_asset SET active=False WHERE path NOT LIKE '%web%' AND path NOT LIKE '%theme%';"""
    )
