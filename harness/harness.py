import os
from dataclasses import dataclass, field
from importlib import import_module
from typing import Tuple, List, Dict, Callable, Optional

from linkml_runtime.loaders import YAMLLoader, JSONLoader
from linkml_runtime.utils.yamlutils import TypedNode
from model.python.integration import Manifest, TestEntry, Module, Comparator, Subset, Filter, \
    ComparatorName, FilterName, ModuleName, SubsetName


def empty_dict():
    return field(default_factory=dict)


def empty_list():
    return field(default_factory=list)


TEST_ID = Tuple[ModuleName, str]

KNOWN_LOADERS = {'yaml': YAMLLoader(),
                 'json': JSONLoader()
                 }


@dataclass
class Harness:
    """
    A testing harness that is loaded from the config_root_dir.
    """
    config_root_dir: str

    # The following variables are loaded post_init
    subsets: Dict[SubsetName, Subset] = empty_dict()
    comparators: Dict[ComparatorName, Comparator] = empty_dict()
    filters: Dict[FilterName, Filter] = empty_dict()
    modules: Dict[ModuleName, Module] = empty_dict()
    tests: Dict[TEST_ID, TestEntry] = empty_dict()

    configuration_files: List[str] = empty_list()
    configuration_errors: List[str] = empty_list()
    configuration_warnings: List[str] = empty_list()

    def __post_init__(self) -> None:
        # Recursively process the manifest configuration files
        self.proc_config_dir(self.config_root_dir)
        self._validate_model()

    # TODO: Replace these with a standard logger module
    def _warning(self, w: str) -> None:
        self.configuration_warnings.append(w)

    def _error(self, e: str) -> None:
        self.configuration_errors.append(e)

    def proc_config_dir(self, dir_or_file_name: str, abs_config_dir:str = None) -> None:
        """ Recursively process all configuration files in dir_or_file_name """
        def add_to_dictionary(source_dict: Dict, target_dict: Dict) -> None:
            for k, v in source_dict.items():
                if k in target_dict and target_dict[k] != v:
                    self._warning(f"{TypedNode.yaml_loc(k)} {type(v).__name__} {k} entry was overwritten")
                target_dict[k] = v

        abs_dir_or_file_name = os.path.abspath(dir_or_file_name)
        is_dir_name = os.path.isdir(abs_dir_or_file_name)
        if abs_config_dir is None:
            abs_config_dir = abs_dir_or_file_name if is_dir_name else os.path.dirname(abs_dir_or_file_name)
        if is_dir_name:
            for filename in os.listdir(abs_dir_or_file_name):
                abs_filename = os.path.join(abs_dir_or_file_name, filename)
                self.proc_config_dir(abs_filename, abs_config_dir)
        else:
            filename = os.path.basename(abs_dir_or_file_name)
            abs_filename = abs_dir_or_file_name
            if '.' in filename:
                suffix = filename.rsplit('.', 1)[1]
                if suffix in KNOWN_LOADERS:
                    rel_filename = os.path.relpath(abs_filename, abs_config_dir)
                    self.configuration_files.append(rel_filename)
                    manifest = KNOWN_LOADERS[suffix].load(abs_filename, Manifest, base_dir=abs_config_dir)
                    add_to_dictionary(manifest.subsets, self.subsets)
                    add_to_dictionary(manifest.comparators, self.comparators)
                    add_to_dictionary(manifest.filters, self.filters)
                    add_to_dictionary(manifest.modules, self.modules)
                    for module_name, testlist in manifest.tests.items():
                        for test_entry in testlist.tests:
                            test_id = (module_name, test_entry.name if test_entry.name else test_entry.target.path)
                            self.tests[test_id] = test_entry

    def resolve_entry_point(self, ep: str) -> Optional[Callable]:
        package, module = ep.split(':') if ':' in ep else ep.rsplit('.', 1) if '.' in ep else (None, ep)
        try:
            m = import_module(package) if package else globals()
        except ModuleNotFoundError as e:
            self._error(f"Unable to load: {ep}: {e.msg}")
            return None
        if hasattr(m, module):
            return getattr(m, module)
        self._error(f"Unrecognized method: {module} in entry_point: {ep}")

    def _validate_model(self) -> None:
        """
        Validate the model components.  Note that warnings still return success
        :return: success indicator
        """
        # If there are no modules, we've clearly missed the boat
        if not self.configuration_files:
            self._error("No valid configuration files were found.  Wrong directory path?")
            return
        # Validate comparators
        for c in self.comparators.values():
            c.method = self.resolve_entry_point(c.entry_point)
        # Validate filters
        for f in self.filters.values():
            f.method = self.resolve_entry_point(f.entry_point)
        # Validate modules
        for m in self.modules.values():
            if m.comparator not in self.comparators:
                self._error(f"Module {m.name}: Unrecognized comparator: {m.comparator}")
            if m.filter not in self.filters:
                self._error(f"Module {m.name}: Unrecognized filter: {m.filter}")
            for m_ss in m.subsets:
                if m_ss not in self.subsets:
                    self._warning(f"Module {m.name}: Unrecognized subset: {m_ss}")
            m.method = self.resolve_entry_point(m.entry_point)

        # Validate individual tests
        for testid, testentry in self.tests.items():
            if testid[0] not in self.modules:
                self._error(f"Testing module {testid[0]} is not defined")
                test_module = None
            else:
                test_module = self.modules[testid[0]]
            for t_ss in testentry.subsets:
                if t_ss not in self.subsets:
                    self._warning(f"Test {testentry.name}: Unrecognized subset: {t_ss}")
            if testentry.comparator:
                if testentry.comparator not in self.comparators:
                    self._error(f"TestEntry {testid}: Unrecognized comparator: {testentry.comparator}")
            elif test_module:
                testentry.comparator = test_module.comparator
            if testentry.filter:
                if testentry.filter not in self.filters:
                    self._error(f"TestEntry {testid}: Unrecognized filter: {testentry.filter}")
            elif test_module:
                testentry.filter = test_module.filter

    def has_errors(self) -> bool:
        return bool(self.configuration_errors)

    def has_warnings(self) -> bool:
        return bool(self.configuration_warnings)

    def details(self) -> str:
        rval = []
        if self.configuration_errors:
            rval.append("Errors:")
            for e in self.configuration_errors:
                rval.append("\t" + e)
            rval.append("")
        if self.configuration_warnings:
            rval.append("Warnings:")
            for w in self.configuration_warnings:
                rval.append("\t" + w)
            rval.append("")
        return "\n".join(rval)

