
from abc import ABC, abstractmethod

class AbsToolFactoryRegistry(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def register(self, tool):
        pass

    @abstractmethod
    def get_tool(self, tool_name):
        pass

class DefaultToolFactoryRegistry(AbsToolFactoryRegistry):
    def __init__(self):
        self.factory_registry = {}
        super().__init__()

    def register(self, name, factory):
        self.factory_registry[name] = factory

    def get_tool(self, factory):
        if factory not in self.factory_registry:
            raise ValueError("ToolFactory not found")
        else:
            return self.factory_registry[factory]

class AbsToolFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_tool(self, name):
        pass

class AbsFuncRegistry(ABC):
    def __init__(self):
        self.func_registry = {}

    def register_tool(self, name, func):
        self.func_registry[name] = func
    
    def get_tool(self, name):
        return self.func_registry[name]
    

class AbsToolFunc(ABC):
    def __init__(self):
        pass

    @staticmethod
    def run(self, args):
        pass