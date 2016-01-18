import txZkConfig

# These parameters must be set here or on the command line
# in order to connect to the zookeeper cluster
config = txZkConfig.get_context("Local")
config.bind_to_zk(servers=["192.168.1.10:2181", ],
                  session_timeout=None,
                  path="/txZkConfigRoot")

# Global Namespace
config.global_param_a = "a"

# ns1 Namespace
config.ns1.param_x = "x"

# ns2 Namespace
config.ns2.param_y = "y"
