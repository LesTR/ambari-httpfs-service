#!/usr/bin/env python
import grp, pwd

from resource_management import *

class Httpfs_component(Script):
    def configure(self, env):
        import params
        Logger.info("Configure HttpFS service")
        try:
            grp.getgrnam(params.httpfs_group)
        except KeyError:
            Logger.info(format("Creating group '{params.httpfs_group}' for HttpFS"))
            Group(
                group_name      = params.httpfs_group,
                ignore_failures = params.ignore_groupsusers_create
            )
        try:
            pwd.getpwnam(params.httpfs_user)
        except KeyError:
            Logger.info(format("Creating user '{params.httpfs_user}' for HttpFS"))
            User(
                username        = params.httpfs_user,
                groups          = [ params.httpfs_group ],
                ignore_failures = params.ignore_groupsusers_create
            )
        Directory( params.httpfs_conf_dir,
            owner     = params.httpfs_user,
            group     = params.httpfs_group,
            create_parents = True,
            mode      = 0755,
        )
        Directory( params.httpfs_log_dir,
            owner     = params.httpfs_user,
            group     = params.httpfs_group,
            create_parents = True,
            mode      = 0755,
        )
        Logger.info( format("Creating {params.httpfs_conf_dir}/httpfs-env.sh config file"))
        File( format("{params.httpfs_conf_dir}/httpfs-env.sh"),
            content   = InlineTemplate(params.httpfs_env_template,
                httpfs_server_port       = params.httpfs_server_port,
                httpfs_server_admin_port = params.httpfs_server_admin_port,
                httpfs_log_dir           = params.httpfs_log_dir
            ),
            owner     = params.httpfs_user,
            group     = params.httpfs_group,
            mode      = 0644
        )
        Logger.info(format("Creating {params.httpfs_conf_dir}/httpfs-env.sh config file - DONE"))
        Logger.info(format("Creating {params.httpfs_conf_dir}/httpfs-site.xml config file"))
        XmlConfig("httpfs-site.xml",
            mode                     = 0644,
            owner                    = params.httpfs_user,
            group                    = params.httpfs_group,
            conf_dir                 = params.httpfs_conf_dir,
            configurations           = params.config['configurations']['httpfs-site'],
            configuration_attributes = params.config['configuration_attributes']['httpfs-site']
        )
        Logger.info(format("Creating {params.httpfs_conf_dir}/httpfs-site.xml config file - DONE"))
        Logger.info(format("Creating {params.httpfs_conf_dir}/httpfs-log4j.properties config file"))
        File(format("{params.httpfs_conf_dir}/httpfs-log4j.properties"),
            mode  = 0644,
            owner = params.httpfs_user,
            group = params.httpfs_group,
            content = params.httpfs_log4j_content
        )
        Logger.info(format("Creating {params.httpfs_conf_dir}/httpfs-log4j.properties config file - Done"))
        Logger.info("Creating symlinks (1/2)")
        Link("/usr/hdp/current/hadoop-httpfs/conf",to = "/etc/hadoop-httpfs/tomcat-deployment/conf")
        Logger.info("Creating symlinks (2/2)")
        Link("/usr/hdp/current/hadoop-httpfs/libexec",to = "/usr/hdp/current/hadoop-client/libexec")
        Logger.info("Creating symlinks - DONE")

    def install(self, env):
        import params
        Logger.info("Installing HttpFS packages")
        self.install_packages(env)
    def stop(self, env):
        Logger.info("Stopping HttpFS service")
        Execute("/usr/hdp/current/hadoop-httpfs/etc/init.d/hadoop-httpfs stop")
    def start(self, env):
        import params
        self.configure(env)
        Logger.info("Starting HttpFS service")
        Execute("/usr/hdp/current/hadoop-httpfs/etc/init.d/hadoop-httpfs start")
    def status(self, env):
        Logger.info("Getting status of HttpFS service")
        try:
            Execute("/usr/hdp/current/hadoop-httpfs/etc/init.d/hadoop-httpfs status")
        except Fail:
            raise ComponentIsNotRunning()

if __name__ == "__main__":
    Httpfs_component().execute()
