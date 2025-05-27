
from openupgradelib import openupgrade

_modules_to_install = ['module_auto_update','sequence_reset_period']

def install_module(env, module):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state='to install'
        WHERE name = '{}' AND state='uninstalled'""".format(module),
    )


@openupgrade.migrate()
def migrate(env, version):

    for mod_name in _modules_to_install:
        if not openupgrade.is_module_installed(env.cr, mod_name):
            install_module(env, mod_name)