import importlib

class NoValue:
    pass

class Namespace(object):

    def __init__(self, name, reserved_attributes=[]):
        self.__dict__['namespace_name'] = name
        self.__dict__['namespace_namespaces'] = dict()
        self.__dict__['namespace_parameters'] = dict()
        for attribute_name in reserved_attributes:
            self.__dict__[attribute_name] = None

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self.namespace_parameters:
            parameter = self.namespace_parameters[name]
            return_val = parameter.value
        elif name in self.namespace_namespaces:
            return_val = self.namespace_namespaces[name]
        else:
            return_val = Namespace(name)
            self.namespace_namespaces[name] = return_val
        return return_val

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self.namespace_parameters:
            parameter = self.namespace_parameters[name]
            parameter.set_value(value)
        else:
            removed_namespace = self.namespace_namespaces.pop(name, None)
            parameter = Parameter(name)
            self.namespace_parameters[name] = parameter
            parameter.set_value(value)

    def get_parameter(self, name):
        if name in self.namespace_parameters:
            return self.namespace_parameters[name]
        else:
            raise NameError

    def get_value(self, name, default=NoValue):
        if name in self.namespace_parameters:
            return self.namespace_parameters.value
        elif default != NoValue:
            return default
        else:
            raise NameError


class Parameter(object):

    def __init__(self, name, value=NoValue):
        self.name = name
        self._value = value

    @property
    def value(self):
        if self._value == NoValue:
            raise NameError
        else:
            return self._value

    def has_value(self):
        return False if self._value == NoValue else True

    def set_value(self, value):
        self._value = value

    def value_or_default(self, default_value):
        return default_value if self._value == NoValue else self._value



class ConfigContext(Namespace):
    contexts = dict()

    def __init__(self, name):
        Namespace.__init__(self, "", ["txzkc_context_name",
                                      "txzkc_servers",
                                      "txzkc_session_timeout",
                                      "txzkc_path"])
        self.txzkc_context_name = name
        self.txzkc_servers = None
        self.txzkc_session_timeout = None
        self.txzkc_path = None

    def bind_to_zk(self, servers, path, session_timeout=None):
        pass


def get_context(context_name):
    return ConfigContext.contexts.setdefault(context_name,
                                             ConfigContext(context_name))

def load_configuration(package_name):
    importlib.import_module(package_name)