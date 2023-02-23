# Auto generated from integration.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-02-21T12:00:25
# Schema: integration
#
# id: https://linkml.org/testing
# description: Model for testing manifest for linkml integration. This model allows the definition of: * modules -
#              major software modules to be tested. This includes loaders, dumpers, generators and other misc
#              tools * subsets - arbitrary tags used for grouping and categorizing tests. Tests cn be selectively
#              run or omitted based on subset membership * comparators - functions that compare expected and
#              actual outputs * filters - functions that can tweak expected and actual output to remove untested
#              portions (dates, versions, etc.) * test sets - collections of tests to be run against a specified
#              module
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = "0.1.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TEST = CurieNamespace('test', 'https://linkml.org/testing/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = TEST


# Types
class Pythonpath(String):
    """ A python style file path, including an optional entry point """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Pythonpath"
    type_model_uri = TEST.Pythonpath


class Unixpath(String):
    """ A unix style path. Usually relative in our situation. """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Unixpath"
    type_model_uri = TEST.Unixpath


# Class references
class SubsetName(extended_str):
    pass


class ComparatorName(extended_str):
    pass


class FilterName(extended_str):
    pass


class ValidatorName(extended_str):
    pass


class ModuleName(extended_str):
    pass


class TestSetModule(ModuleName):
    pass


@dataclass
class Filepath(YAMLRoot):
    """
    A relative path to a file or directory.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Filepath
    class_class_curie: ClassVar[str] = "test:Filepath"
    class_name: ClassVar[str] = "Filepath"
    class_model_uri: ClassVar[URIRef] = TEST.Filepath

    path: Union[str, Unixpath] = None
    is_directory: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.path):
            self.MissingRequiredField("path")
        if not isinstance(self.path, Unixpath):
            self.path = Unixpath(self.path)

        if self.is_directory is not None and not isinstance(self.is_directory, Bool):
            self.is_directory = Bool(self.is_directory)

        super().__post_init__(**kwargs)


@dataclass
class Subset(YAMLRoot):
    """
    A tag used to categorize modules and tests
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Subset
    class_class_curie: ClassVar[str] = "test:Subset"
    class_name: ClassVar[str] = "Subset"
    class_model_uri: ClassVar[URIRef] = TEST.Subset

    name: Union[str, SubsetName] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None and len(kwargs) == 1:
            for k in kwargs:
                self.name = k
                self.description = kwargs[k]
                kwargs = {}
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SubsetName):
            self.name = SubsetName(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Comparator(YAMLRoot):
    """
    Output comparator. Signature: comparator(expected: str, actual: str) -> Optional[str]
    An empty / null return indicates success. Non-compare returns a description of the difference
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Comparator
    class_class_curie: ClassVar[str] = "test:Comparator"
    class_name: ClassVar[str] = "Comparator"
    class_model_uri: ClassVar[URIRef] = TEST.Comparator

    name: Union[str, ComparatorName] = None
    entry_point: str = None
    description: Optional[str] = None
    method: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ComparatorName):
            self.name = ComparatorName(self.name)

        if self._is_empty(self.entry_point):
            self.MissingRequiredField("entry_point")
        if not isinstance(self.entry_point, str):
            self.entry_point = str(self.entry_point)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        super().__post_init__(**kwargs)


@dataclass
class Filter(YAMLRoot):
    """
    Both newly generated output and existing data are run through this filter before comparison.
    In addition, existing data is run through this filter before being written.  The primary purpose
    of the filter is to remove location and temporal metadata from the output files.
    Signature: filter(txt: str) -> str
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Filter
    class_class_curie: ClassVar[str] = "test:Filter"
    class_name: ClassVar[str] = "Filter"
    class_model_uri: ClassVar[URIRef] = TEST.Filter

    name: Union[str, FilterName] = None
    entry_point: str = None
    description: Optional[str] = None
    method: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, FilterName):
            self.name = FilterName(self.name)

        if self._is_empty(self.entry_point):
            self.MissingRequiredField("entry_point")
        if not isinstance(self.entry_point, str):
            self.entry_point = str(self.entry_point)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        super().__post_init__(**kwargs)


@dataclass
class Validator(YAMLRoot):
    """
    Content validation. Used to determine whether the output parses in the target language
    Signature: validator(txt: str) -> Optional[str]"
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Validator
    class_class_curie: ClassVar[str] = "test:Validator"
    class_name: ClassVar[str] = "Validator"
    class_model_uri: ClassVar[URIRef] = TEST.Validator

    name: Union[str, ValidatorName] = None
    entry_point: str = None
    description: Optional[str] = None
    method: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ValidatorName):
            self.name = ValidatorName(self.name)

        if self._is_empty(self.entry_point):
            self.MissingRequiredField("entry_point")
        if not isinstance(self.entry_point, str):
            self.entry_point = str(self.entry_point)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        super().__post_init__(**kwargs)


@dataclass
class Module(YAMLRoot):
    """
    The formal description of a LinkML software module to be tested.  Each module is referenced in the
    TestSet, accompanied by the set of tests that are run against it
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Module
    class_class_curie: ClassVar[str] = "test:Module"
    class_name: ClassVar[str] = "Module"
    class_model_uri: ClassVar[URIRef] = TEST.Module

    name: Union[str, ModuleName] = None
    entry_point: Union[str, Pythonpath] = None
    entry_type: Union[str, "ModuleCallers"] = None
    description: Optional[str] = None
    method: Optional[str] = None
    filter: Optional[Union[str, FilterName]] = "identity_filter"
    comparator: Optional[Union[str, ComparatorName]] = "string_comparator"
    subsets: Optional[Union[Union[str, SubsetName], List[Union[str, SubsetName]]]] = empty_list()
    skip: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ModuleName):
            self.name = ModuleName(self.name)

        if self._is_empty(self.entry_point):
            self.MissingRequiredField("entry_point")
        if not isinstance(self.entry_point, Pythonpath):
            self.entry_point = Pythonpath(self.entry_point)

        if self._is_empty(self.entry_type):
            self.MissingRequiredField("entry_type")
        if not isinstance(self.entry_type, ModuleCallers):
            self.entry_type = ModuleCallers(self.entry_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        if self.filter is not None and not isinstance(self.filter, FilterName):
            self.filter = FilterName(self.filter)

        if self.comparator is not None and not isinstance(self.comparator, ComparatorName):
            self.comparator = ComparatorName(self.comparator)

        if not isinstance(self.subsets, list):
            self.subsets = [self.subsets] if self.subsets is not None else []
        self.subsets = [v if isinstance(v, SubsetName) else SubsetName(v) for v in self.subsets]

        if self.skip is not None and not isinstance(self.skip, Bool):
            self.skip = Bool(self.skip)

        super().__post_init__(**kwargs)


@dataclass
class TestEntry(YAMLRoot):
    """
    A specific test to be executed in the context of a module
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.TestEntry
    class_class_curie: ClassVar[str] = "test:TestEntry"
    class_name: ClassVar[str] = "TestEntry"
    class_model_uri: ClassVar[URIRef] = TEST.TestEntry

    target: Union[dict, Filepath] = None
    name: Optional[str] = None
    description: Optional[str] = None
    issues: Optional[Union[str, List[str]]] = empty_list()
    source: Optional[Union[dict, Filepath]] = None
    parameters: Optional[str] = None
    use_stdout: Optional[Union[bool, Bool]] = False
    fail_text: Optional[Union[str, List[str]]] = empty_list()
    subsets: Optional[Union[Union[str, SubsetName], List[Union[str, SubsetName]]]] = empty_list()
    skip: Optional[Union[bool, Bool]] = False
    filter: Optional[Union[str, FilterName]] = None
    comparator: Optional[Union[str, ComparatorName]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.target):
            self.MissingRequiredField("target")
        if not isinstance(self.target, Filepath):
            self.target = self._normalize_assignment(self.target, Filepath)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.issues, list):
            self.issues = [self.issues] if self.issues is not None else []
        self.issues = [v if isinstance(v, str) else str(v) for v in self.issues]

        if self.source is not None and not isinstance(self.source, Filepath):
            self.source = self._normalize_assignment(self.source, Filepath)

        if self.parameters is not None and not isinstance(self.parameters, str):
            self.parameters = str(self.parameters)

        if self.use_stdout is not None and not isinstance(self.use_stdout, Bool):
            self.use_stdout = Bool(self.use_stdout)

        if not isinstance(self.fail_text, list):
            self.fail_text = [self.fail_text] if self.fail_text is not None else []
        self.fail_text = [v if isinstance(v, str) else str(v) for v in self.fail_text]

        if not isinstance(self.subsets, list):
            self.subsets = [self.subsets] if self.subsets is not None else []
        self.subsets = [v if isinstance(v, SubsetName) else SubsetName(v) for v in self.subsets]

        if self.skip is not None and not isinstance(self.skip, Bool):
            self.skip = Bool(self.skip)

        if self.filter is not None and not isinstance(self.filter, FilterName):
            self.filter = FilterName(self.filter)

        if self.comparator is not None and not isinstance(self.comparator, ComparatorName):
            self.comparator = ComparatorName(self.comparator)

        super().__post_init__(**kwargs)


@dataclass
class TestSet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.TestSet
    class_class_curie: ClassVar[str] = "test:TestSet"
    class_name: ClassVar[str] = "TestSet"
    class_model_uri: ClassVar[URIRef] = TEST.TestSet

    module: Union[str, TestSetModule] = None
    tests: Optional[Union[Union[dict, TestEntry], List[Union[dict, TestEntry]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.module is None and len(kwargs) == 1:
            for k in kwargs:
                self.module = k
                self.tests = kwargs[k]
                kwargs = {}
        if self._is_empty(self.module):
            self.MissingRequiredField("module")
        if not isinstance(self.module, TestSetModule):
            self.module = TestSetModule(self.module)

        if not isinstance(self.tests, list):
            self.tests = [self.tests] if self.tests is not None else []
        self.tests = [v if isinstance(v, TestEntry) else self._normalize_assignment(v, TestEntry) for v in self.tests]

        super().__post_init__(**kwargs)


@dataclass
class Manifest(YAMLRoot):
    """
    A collection of Subsets, modules, comparators, and/or a manifest
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Manifest
    class_class_curie: ClassVar[str] = "test:Manifest"
    class_name: ClassVar[str] = "Manifest"
    class_model_uri: ClassVar[URIRef] = TEST.Manifest

    description: Optional[str] = None
    subsets: Optional[Union[Dict[Union[str, SubsetName], Union[dict, Subset]], List[Union[dict, Subset]]]] = empty_dict()
    comparators: Optional[Union[Dict[Union[str, ComparatorName], Union[dict, Comparator]], List[Union[dict, Comparator]]]] = empty_dict()
    filters: Optional[Union[Dict[Union[str, FilterName], Union[dict, Filter]], List[Union[dict, Filter]]]] = empty_dict()
    modules: Optional[Union[Dict[Union[str, ModuleName], Union[dict, Module]], List[Union[dict, Module]]]] = empty_dict()
    tests: Optional[Union[Dict[Union[str, TestSetModule], Union[dict, TestSet]], List[Union[dict, TestSet]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not self.subsets and kwargs:
            self.subsets = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="subsets", slot_type=Subset, key_name="name", keyed=True)

        if not self.comparators and kwargs:
            self.comparators = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="comparators", slot_type=Comparator, key_name="name", keyed=True)

        if not self.filters and kwargs:
            self.filters = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="filters", slot_type=Filter, key_name="name", keyed=True)

        if not self.modules and kwargs:
            self.modules = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="modules", slot_type=Module, key_name="name", keyed=True)

        if not self.tests and kwargs:
            self.tests = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="tests", slot_type=TestSet, key_name="module", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations
class ModuleCallers(EnumDefinitionImpl):
    """
    Wrapper code for various modules
    """
    Loader = PermissibleValue(text="Loader")
    Dumper = PermissibleValue(text="Dumper")
    Generator = PermissibleValue(text="Generator")

    _defn = EnumDefinition(
        name="ModuleCallers",
        description="Wrapper code for various modules",
    )

# Slots

