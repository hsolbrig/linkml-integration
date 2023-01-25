# Auto generated from test.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-01-06T16:30:52
# Schema: testing
#
# id: https://linkml.org/testing
# description:
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
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = "0.1.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TEST = CurieNamespace('test', 'https://linkml.org/testing/')
DEFAULT_ = TEST


# Types

# Class references
class KvName(extended_str):
    pass


@dataclass
class Kv(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Kv
    class_class_curie: ClassVar[str] = "test:Kv"
    class_name: ClassVar[str] = "Kv"
    class_model_uri: ClassVar[URIRef] = TEST.Kv

    name: Union[str, KvName] = None
    value: Optional[str] = None
    another_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KvName):
            self.name = KvName(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.another_value is not None and not isinstance(self.another_value, str):
            self.another_value = str(self.another_value)

        super().__post_init__(**kwargs)


@dataclass
class Kvs(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Kvs
    class_class_curie: ClassVar[str] = "test:Kvs"
    class_name: ClassVar[str] = "Kvs"
    class_model_uri: ClassVar[URIRef] = TEST.Kvs

    entry: Optional[Union[Dict[Union[str, KvName], Union[dict, Kv]], List[Union[dict, Kv]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not self.entry and kwargs:
            self.entry = kwargs
            kwargs = {}
        self._normalize_inlined_as_dict(slot_name="entry", slot_type=Kv, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Kvls(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEST.Kvls
    class_class_curie: ClassVar[str] = "test:Kvls"
    class_name: ClassVar[str] = "Kvls"
    class_model_uri: ClassVar[URIRef] = TEST.Kvls

    entry: Optional[Union[Dict[Union[str, KvName], Union[dict, Kv]], List[Union[dict, Kv]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not self.entry and kwargs:
            self.entry = kwargs
            kwargs = {}
        self._normalize_inlined_as_list(slot_name="entry", slot_type=Kv, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

