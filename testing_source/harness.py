import os
import shlex
import sys
from contextlib import redirect_stdout, redirect_stderr
from importlib import import_module
from io import StringIO
from typing import Optional, Tuple, Callable, List, Dict

from linkml_runtime.loaders import YAMLLoader
from model.integration import Manifest, TestEntry, Filepath, Module, Comparator, Subset, TestSet, Filter
from support import click_tweaker
from testing_source import CONFIG_PATH, INPUT_BASE, OUTPUT_BASE, TEMP_BASE
from testing_source.run_log import RunLog
from testing_source.support.dirutils import make_testing_directory, make_output_directory_for

# The following comparators are dynamically invoked, so force presence below
from support.basic_comparators import string_comparator, jsonld_comparator, always_pass_comparator, n3_comparator
from support.python_comparator import compare_python, validate_python
from support.compare_rdf import compare_rdf
_ = string_comparator, jsonld_comparator, always_pass_comparator, compare_python, validate_python, compare_rdf, \
    n3_comparator
from support.filters import ldcontext_metadata_filter, identity_filter, nb_filter, yaml_filter, metadata_filter, \
    json_metadata_filter, json_metadata_context_filter
__ = ldcontext_metadata_filter, identity_filter, nb_filter, yaml_filter, metadata_filter, json_metadata_filter, \
    json_metadata_context_filter

class Harness:
    loader: YAMLLoader = YAMLLoader()

    def __init__(self):
        self.subsets: Dict[str, Subset] = self.loader.load_any('subsets.yaml', Manifest, base_dir=CONFIG_PATH).subsets
        self.comparators: Dict[str, Comparator] = self.loader.load_any('comparators.yaml',
                                                                  Manifest, base_dir=CONFIG_PATH).comparators
        self.filters: Dict[str, Filter] = self.loader.load_any('filters.yaml', Manifest, base_dir=CONFIG_PATH).filters
        self.modules: Dict[str, Module] = self.loader.load_any('modules.yaml', Manifest, base_dir=CONFIG_PATH).modules
        self.tests: Dict[str, TestSet] = YAMLLoader().load_any('manifest.yaml', Manifest, base_dir=CONFIG_PATH).tests

        self.run_log = RunLog()
        self.module_info: Optional[Module] = None
        self.module_comparator: Optional[Callable[[str, str], str]] = None

        make_testing_directory(TEMP_BASE, clear=True)
        make_output_directory_for(OUTPUT_BASE, is_directory=True)

        # Eventually we will make this a separate operation
        self.errors = self.validate_model()

    def validate_model(self) -> List[str]:
        """ Validate the model components """
        # Make sure all named comparators exist
        errors = []
        for c in self.comparators.values():
            if c.entry_point not in globals():
                errors.append(f"Comparator {c.name}: Undefined entry point: {c.entry_point}")
        for f in self.filters.values():
            if f.entry_point not in globals():
                errors.append(f"Filter {f.name}: Undefined entry point: {f.entry_point}")
        for m in self.modules.values():
            if not m.comparator:
                m.comparator = string_comparator.__name__
            if m.comparator not in self.comparators:
                errors.append(f"Module {m.name}: Unrecognized comparator: {m.comparator}")
            for m_ss in m.subsets:
                if m_ss not in self.subsets:
                    errors.append(f"Module {m.name}: Unrecognized subset: {m_ss}")
            for ts in self.tests.values():
                if ts.module not in self.modules:
                    errors.append(f"Testing module {ts.module} is not defined")
                for t in ts.tests:
                    for t_ss in t.subsets:
                        if t_ss not in self.subsets:
                            errors.append(f"Test {t.name}: Unrecognized subset: {t_ss}")
        return errors

    def set_testing_module(self, module_name: str) -> None:
        """ Set up the environment for testing a module """
        self.module_info = self.modules[module_name]
        if self.module_info.comparator not in self.comparators:
            raise ValueError(f"Module {module_name}: unrecognized comparator: {self.module_info.comparator}")
        self.module_comparator = globals().get(self.comparators[self.module_info.comparator].entry_point)
        if not self.module_comparator:
            raise ValueError(f"Unrecognized comparator entry point "
                             f"({self.comparators[self.module_info.comparator].entry_point} "
                             f"for model {self.module_info.name}")

    def source_path(self, source: Optional[Filepath]) -> str:
        return os.path.join(INPUT_BASE, source.path) if source else None

    def target_path(self, target: Filepath) -> Tuple[str, str]:
        """ Return two paths - one to the expected output, the second to the actual """
        expected = os.path.join(OUTPUT_BASE, self.module_info.name, target.path)
        actual = os.path.join(TEMP_BASE, self.module_info.name, target.path)
        # TODO: Is the following line needed?
        os.makedirs(actual if target.is_directory else os.path.dirname(actual), exist_ok=True)
        return expected, actual

    def evaluate_output(self, test: TestEntry, stdout: str, stderr: str, expected_fname: str, actual_fname: str) -> None:
        """ Evaluate the output and act accordingly """
        if not test.use_stdout:
            with open(actual_fname) as ef:
                actual_text = ef.read()
        else:
            actual_text = stdout

        if os.path.exists(expected_fname):
            with open(expected_fname) as af:
                expected_text = af.read()
            compare_result = self.module_comparator(expected_text, actual_text)
            if compare_result:
                self.run_log.log_file_mismatch(self.module_info, test, expected_fname, compare_result)
            else:
                self.run_log.log_success(self.module_info, test)
        else:
            make_output_directory_for(expected_fname, is_directory=test.target.is_directory)
            with open(expected_fname, 'w') as exnew:
                exnew.write(actual_text)
            self.run_log.log_new_test(self.module_info, test, expected_fname)

    def run(self, check_errors: bool=True):
        """ Iterate over the various tests """
        if check_errors and self.errors:
            print('\n'.join(self.errors))
            return
        for module_name, test_list in self.tests.items():
            self.set_testing_module(module_name)
            make_output_directory_for(os.path.join(OUTPUT_BASE, module_name), is_directory=True)
            m_name, ep_name = self.module_info.entry_point.split(':', 1) \
                if ':' in self.module_info.entry_point else (self.module_info.entry_point, 'main')
            module = import_module(m_name, '..submodules')
            ep = getattr(module, ep_name)

            test: TestEntry
            for test in test_list.tests:
                self.run_log.start_test()
                source_path = self.source_path(test.source)
                expected_path, actual_path = self.target_path(test.target)
                param_str = (test.parameters or "").format(outfile=actual_path)
                parms = ([source_path] if source_path else []) + shlex.split(param_str)

                stdout = StringIO()
                stderr = StringIO()
                with redirect_stderr(stderr):
                    with redirect_stdout(stdout):
                        try:
                            ep(parms, prog_name=module_name)
                        except click_tweaker.CLIExitException:
                            pass

                self.evaluate_output(test, stdout.getvalue(), stderr.getvalue(), expected_path, actual_path)

        print(str(self.run_log))


