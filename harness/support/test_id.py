from typing import Union

from model.python.integration import Module, TestEntry, ModuleName


class TestID:
    def __init__(self, module: Union[Module, ModuleName], test: TestEntry) -> None:
        self.module_name = module.name if isinstance(module, Module) else module
        self.test_name = test.name if test.name else test.target.path

    def __str__(self) -> str:
        return self.module_name + ":" + self.test_name
