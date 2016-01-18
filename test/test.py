from twisted.trial import unittest

import txZkConfig


class TestGetLocalValues(unittest.TestCase):
    def setUp(self):
        txZkConfig.load_configuration("example_config")
        self.config_context = txZkConfig.get_context("Local")

    def tearDown(self):
        pass

    def test_local_value(self):
        self.failUnlessEqual(self.config_context.global_param_a, "a")

    def test_parameter_local_value(self):
        parameter = self.config_context.get_parameter("global_param_a")
        self.failUnlessEqual(parameter.value, "a")

    def test_parameter_local_default(self):
        config_value = self.config_context.get_value("global_missing", default="default_value")
        self.failUnlessEqual(config_value, "default_value")

    def test_missing_parameter(self):
        try:
            self.config_context.get_parameter("doesnt_exist")
            self.fail()
        except Exception as err:
            self.failUnlessIsInstance(err, NameError)

    def test_namespace_value(self):
        self.failUnlessEqual(self.config_context.ns1.param_x, "x")

    def test_namespace_parameter(self):
        parameter = self.config_context.ns2.get_parameter("param_y")
        self.failUnlessEqual(parameter.value, "y")


class TestZkBind(unittest.TestCase):
    pass
