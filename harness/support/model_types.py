""" Types used in the integration harness """
from typing import Tuple

from model.integration import TestEntryName, ModuleName

TestEntry_Key = Tuple[ModuleName, TestEntryName]
