from abc import ABC, abstractmethod

from ...common import factory

class PdfToolFactory(factory.AbsToolFactory, factory.AbsFuncRegistry):
    def __init__(self):
        factory.AbsFuncRegistry.__init__(self)

    def create_tool(self, name):
        if name in self.func_registry:
            return self.get_tool(name)
        else:
            raise ValueError("Invalid tool name")
        

