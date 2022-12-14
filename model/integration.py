# Auto generated from integration.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-12-14T15:39:24
# Schema: integration
#
# id: https://linkml.org/testing
# description: Testing harness for linkml integration testing
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
    """ A python style path """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Pythonpath"
    type_model_uri = TEST.Pythonpath


class Unixpath(String):
    """ A unix style path """
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


class ModuleName(extended_str):
    pass


class TestSetModule(ModuleName):
    pass


@dataclass
class Filepath(YAMLRoot):
    """
    a relative path to a file or directory
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
    Categorization of type of test
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Subset
    class_class_curie: ClassVar[str] = "test:Subset"
    class_name: ClassVar[str] = "Subset"
    class_model_uri: ClassVar[URIRef] = TEST.Subset

    name: Union[str, SubsetName] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
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
    Output comparator
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Comparator
    class_class_curie: ClassVar[str] = "test:Comparator"
    class_name: ClassVar[str] = "Comparator"
    class_model_uri: ClassVar[URIRef] = TEST.Comparator

    name: Union[str, ComparatorName] = None
    entry_point: str = None
    description: Optional[str] = None

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

        super().__post_init__(**kwargs)


@dataclass
class Filter(YAMLRoot):
    """
    Pre comparison filters
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Filter
    class_class_curie: ClassVar[str] = "test:Filter"
    class_name: ClassVar[str] = "Filter"
    class_model_uri: ClassVar[URIRef] = TEST.Filter

    name: Union[str, FilterName] = None
    entry_point: str = None
    description: Optional[str] = None

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

        super().__post_init__(**kwargs)


@dataclass
class Module(YAMLRoot):
    """
    LinkML software module to be tested
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Module
    class_class_curie: ClassVar[str] = "test:Module"
    class_name: ClassVar[str] = "Module"
    class_model_uri: ClassVar[URIRef] = TEST.Module

    name: Union[str, ModuleName] = None
    entry_point: Union[str, Pythonpath] = None
    description: Optional[str] = None
    filter: Optional[Union[str, Pythonpath]] = "\"identity_filter\""
    comparator: Optional[Union[str, ComparatorName]] = "\"string_comparator\""
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

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.filter is not None and not isinstance(self.filter, Pythonpath):
            self.filter = Pythonpath(self.filter)

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
    description: Optional[str] = None
    issues: Optional[Union[str, List[str]]] = empty_list()
    source: Optional[Union[dict, Filepath]] = None
    parameters: Optional[str] = None
    use_stdout: Optional[Union[bool, Bool]] = False
    fail_text: Optional[Union[str, List[str]]] = empty_list()
    subsets: Optional[Union[Union[str, SubsetName], List[Union[str, SubsetName]]]] = empty_list()
    skip: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.target):
            self.MissingRequiredField("target")
        if not isinstance(self.target, Filepath):
            self.target = Filepath(**as_dict(self.target))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.issues, list):
            self.issues = [self.issues] if self.issues is not None else []
        self.issues = [v if isinstance(v, str) else str(v) for v in self.issues]

        if self.source is not None and not isinstance(self.source, Filepath):
            self.source = Filepath(**as_dict(self.source))

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
        if self._is_empty(self.module):
            self.MissingRequiredField("module")
        if not isinstance(self.module, TestSetModule):
            self.module = TestSetModule(self.module)

        if not isinstance(self.tests, list):
            self.tests = [self.tests] if self.tests is not None else []
        self.tests = [v if isinstance(v, TestEntry) else TestEntry(**as_dict(v)) for v in self.tests]

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

        self._normalize_inlined_as_dict(slot_name="subsets", slot_type=Subset, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="comparators", slot_type=Comparator, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="filters", slot_type=Filter, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="modules", slot_type=Module, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="tests", slot_type=TestSet, key_name="module", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

