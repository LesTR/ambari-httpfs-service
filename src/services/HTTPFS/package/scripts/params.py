from resource_management import *
config = Script.get_config()

ignore_groupsusers_create = default("/configurations/cluster-env/ignore_groupsusers_create", False)
smoke_user                = default("/configurations/cluster-env/smokeuser","ambari-qa")

httpfs_user               = config['configurations']['httpfs']['user']
httpfs_group              = config['configurations']['httpfs']['group']
httpfs_conf_dir           = config['configurations']['httpfs']['conf_dir']

httpfs_server_port        = config['configurations']['httpfs']['port']
httpfs_server_admin_port  = config['configurations']['httpfs']['admin.port']
httpfs_log_dir            = config['configurations']['httpfs']['httpfs_log_dir']

httpfs_env_template       = config['configurations']['httpfs-env']['content']
httpfs_log4j_content      = config['configurations']['httpfs-log4j']['content']

