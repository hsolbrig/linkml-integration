import os
import shlex
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
from typing import List, Tuple, cast, Callable, Any

from harness.harness import Harness, empty_list
from harness.run_log import RunLog
from harness.support.dirutils import make_guarded_directory
from model.python.integration import ModuleName, SubsetName, TestEntry, Filepath, Module, ModuleCallers


@dataclass
class HarnessRunner:
    """ Module to execute the set of tests in a harness """
    harness: Harness
    source_root_dir: str
    expected_output_root_dir: str
    actual_output_root_dir: str

    stop_on_error: bool = False
    run_one_test: bool = False
    print_progress: bool = False
    only_modules: List[ModuleName] = empty_list()
    exclude_modules: List[ModuleName] = empty_list()
    only_subsets: List[SubsetName] = empty_list()
    exclude_subsets: List[SubsetName] = empty_list()
    only_tests: List[str] = empty_list()
    exclude_tests: List[str] = empty_list()

    run_log: RunLog = None

    errors: List[str] = empty_list()
    warnings: List[str] = empty_list()
    progress: List[str] = empty_list()

    def __post_init__(self):
        self.only_modules = [m if isinstance(m, ModuleName) else ModuleName(m) for m in self.only_modules]
        self.exclude_modules = [m if isinstance(m, ModuleName) else ModuleName(m) for m in self.exclude_modules]
        self.only_subsets = [s if isinstance(s, SubsetName) else ModuleName(s) for s in self.only_subsets]
        self.exclude_subsets = [s if isinstance(s, SubsetName) else ModuleName(s) for s in self.exclude_subsets]
        self.run_log = RunLog(self.expected_output_root_dir)

    def _error(self, msg: str) -> None:
        self.errors.append(msg)

    def _warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def _log(self, msg: str) -> None:
        if self.print_progress:
            print(msg)
        self.progress.append(msg)

    def validate_parameters(self) -> bool:
        """ Return true if parameters are valid """
        def _check_valid(entries: List, target, typ: str) -> None:
            for e in entries:
                if e not in target:
                    self._error(f"Unrecognized {typ} name: {e}")

        def _check_valid_testname(entries: List[str]) -> None:
            for e in entries:
                hit = False
                for k in self.harness.tests.keys():
                    if e == k[1]:
                        hit = True
                        break
                if not hit:
                    self._error(f"Unrecognized test name: {e}")

        _check_valid(self.only_modules, self.harness.modules, "module")
        _check_valid(self.exclude_modules, self.harness.modules, "module")
        _check_valid(self.only_subsets, self.harness.subsets, "subset")
        _check_valid(self.exclude_subsets, self.harness.subsets, "subset")
        _check_valid_testname(self.only_tests)
        _check_valid_testname(self.exclude_tests)

        if not os.path.exists(self.actual_output_root_dir):
            self._error(f"Output root directory ({self.actual_output_root_dir}) does not exist exist")
        if not os.path.exists(self.expected_output_root_dir):
            self._error(f"Expected output root directory ({self.expected_output_root_dir}) does not exist")

        return not bool(self.errors)

    def run(self) -> bool:
        if not self.validate_parameters():
            return False

        for k, test_entry in self.harness.tests.items():
            module = self.harness.modules[k[0]]
            test_name = k[1]
            test_description = f"Module: {module.name}, test: {test_name}"
            if module.skip or \
                test_entry.skip or \
                (self.only_modules and module.name not in self.only_modules) or\
                module.name in self.exclude_modules or \
                    (self.only_subsets and not (test_entry.subsets and self.only_subsets)) or \
                    (self.exclude_subsets and (test_entry.subsets and self.exclude_subsets)):
                self._log(f"{test_description} skipped")
                break
            if not self.run_test(test_description, test_entry, module) and self.stop_on_error or self.run_one_test:
                break

    def run_test(self, test_description: str, test_entry: TestEntry, module: Module) -> bool:
        """
        Run a single TestEntry test
        :param test_description: Textual name of the test
        :param test_entry: Test description
        :param module: Test module
        :return: True if success, False if error
        """
        self._log(f"Running {test_description}")
        if (not test_entry.source or not test_entry.source.is_directory) and not test_entry.target.is_directory:
            return self.proc_single_file(test_entry, module)
        return False

    def proc_single_file(self, test_entry: TestEntry, module: Module) -> bool:
        source_path = os.path.join(self.source_root_dir, test_entry.source.path) if test_entry.source else None
        expected_path, actual_path = self.target_path(module, test_entry.target)
        param_str = (test_entry.parameters or "").format(outfile=actual_path)
        parms = ([source_path] if source_path else []) + shlex.split(param_str)
        self.run_log.start_test(module, test_entry)
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stderr(stderr):
            with redirect_stdout(stdout):
                # TODO: simplify this once permissible values get identity
                method = cast(Callable, module.method)
                match str(module.entry_type):
                    case ModuleCallers.Generator.text:
                        method(parms, standalone_mode=False, prog_name=module.name)
                    case _:
                        self._error(f"Unknown module entry_type: {module.entry_type}")
                        return False
        return self.evaluate_output(module,
                                    test_entry,
                                    stdout.getvalue(),
                                    stderr.getvalue(),
                                    expected_path,
                                    actual_path)

    def evaluate_output(self,
                        module: Module,
                        test: TestEntry,
                        stdout: str,
                        stderr: str,
                        expected_fname: str,
                        actual_fname: str) -> bool:
        """ Evaluate the output and act accordingly """
        if not test.use_stdout:
            with open(actual_fname) as ef:
                actual_text = ef.read()
        else:
            actual_text = stdout

        # TODO: Think about how to get this into the declaration
        comparator = cast(Callable[[Any, Any], str], self.harness.comparators[module.comparator].method)
        filtr = cast(Callable[[any], Any], self.harness.filters[module.filter].method)

        if stderr:
            return self.run_log.unexpected_stderr_output(module, test, stderr)

        elif os.path.exists(expected_fname):
            with open(expected_fname) as ef:
                expected_text = ef.read()
            compare_result = comparator(filtr(expected_text), filtr(actual_text))
            if compare_result:
                return self.run_log.output_mismatch(compare_result)
            else:
                return self.run_log.success()

        else:
            os.makedirs(os.path.dirname(expected_fname), exist_ok=True)
            with open(expected_fname, 'w') as exnew:
                exnew.write(actual_text)
            return self.run_log.new_output_file()

    # def _validate_options(self,
    #                       modules: Optional[List[ModuleName]],
    #                       subsets: Optional[List[SubsetName]],
    #                       tests: Optional[List[Tuple[ModuleName, str]]]) -> bool:
    #     """
    #     Validate input options and print errors on sys.stderr
    #     :param modules: list of modules to test
    #     :param subsets: list of subsets to test
    #     :param tests: list of specific tests to run
    #     :return: True if errors exist
    #     """
    #     error_list = []
    #     # Validate the inputs
    #     if modules:
    #         for m in modules:
    #             if m not in self.modules:
    #                 error_list.append(f"Unrecognized module: {m}")
    #         for s in subsets:
    #             if s not in self.subsets:
    #                 error_list.append(f"Unrecognized subset: {s}")
    #         for t in tests:
    #             if t[0] and t[0] not in self.modules:
    #                 error_list.append(f"Unrecognized module for test: {t[0]}.{t[1]}")
    #             elif t[0]:
    #                 if t[1] not in self.tests[t[0]]:
    #                     pass
    def target_path(self, module: Module, target: Filepath) -> Tuple[str, str]:
        """ Return two paths - one to the expected output, the second to the actual """
        expected = os.path.join(self.expected_output_root_dir, module.name, target.path)
        actual = os.path.join(self.actual_output_root_dir, module.name, target.path)
        if target.is_directory:
            make_guarded_directory(self.actual_output_root_dir,
                                   [module.name, target.path],
                                   clear=True)
        else:
            make_guarded_directory(self.actual_output_root_dir,
                                   [module.name, os.path.dirname(target.path)],
                                   clear=False)
        return expected, actual

        #                     source_path = self.source_path(test.source)
        #                     expected_path, actual_path = self.target_path(test.target)
        #                     param_str = (test.parameters or "").format(outfile=actual_path)
        #                     parms = ([source_path] if source_path else []) + shlex.split(param_str)
        #
        #                     stdout = StringIO()
        #                     stderr = StringIO()
        #                     with redirect_stderr(stderr):
        #                         with redirect_stdout(stdout):
        #                             try:
        #                                 ep(parms, prog_name=module_name)
        #                             except click_tweaker.CLIExitException:
        #                                 pass
        #
        #                     self.evaluate_output(test, stdout.getvalue(), stderr.getvalue(), expected_path, actual_path)
        #                 else:
        #                     self.run_log.log_skipped_test(module_name, test)


    #
    # def set_testing_module(self, module_name: str) -> bool:
    #     """
    #     Set the enviroment for module_name
    #     :param module_name: Module to test
    #     :return: True if test is to be executed
    #     """
    #     self.module_info = self.modules[module_name]
    #     if not self.module_info.skip:
    #         # Establish defaults
    #         if self.module_info.comparator not in self.comparators:
    #             raise ValueError(f"Module {module_name}: unrecognized comparator: {self.module_info.comparator}")
    #         self.module_comparator = globals().get(self.comparators[self.module_info.comparator].entry_point)
    #         if not self.module_comparator:
    #             raise ValueError(f"Unrecognized comparator entry point "
    #                              f"({self.comparators[self.module_info.comparator].entry_point} "
    #                              f"for model {self.module_info.name}")
    #         if self.module_info.filter not in self.filters:
    #             raise ValueError(f"Module {module_name}: unrecognized filter: {self.module_info.filter}")
    #         self.module_filter = globals().get(self.filters[self.module_info.filter].entry_point)
    #         if not self.module_filter:
    #             raise ValueError(f"Unrecognized filter entry point "
    #                              f"({self.filters[self.module_info.filter].entry_point} "
    #                              f"for model {self.module_info.name}")
    #         return True
    #     else:
    #         self.run_log.log_skipped_module(module_name)
    #         return False
    #
    # def source_path(self, source: Optional[Filepath]) -> str:
    #     return os.path.join(INPUT_BASE, source.path) if source else None
    #

    #

    #
    #
    #
    # def run(self, *, fail_on_error: bool = False,
    #         modules: Optional[List[str]] = None,
    #         subsets: Optional[List[str]] = None,
    #         tests: Optional[List[str]] = None) -> "Harness":
    #     """
    #     Iterate over the various tests
    #     :param fail_on_error: True means stop if error is encountered
    #     :param modules: Name(s) of specific modules to test
    #     :param subsets: Name(s) of specific subsets to test
    #     :param tests: Name(s) of specific tests to run.  Format: <module name>.<test name>
    #     :return: Harness instance
    #     """
    #     # Validate the input parameters
    #     self._validate_options(modules, subsets, tests)
    #     for module_name, test_list in self.tests.items():
    #         if self.set_testing_module(module_name):
    #             make_expected_directory(os.path.join(OUTPUT_BASE, module_name), is_directory=True)
    #             m_name, ep_name = self.module_info.entry_point.split(':', 1) \
    #                 if ':' in self.module_info.entry_point else (self.module_info.entry_point, 'main')
    #             module = import_module(m_name, '..submodules')
    #             ep = getattr(module, ep_name)
    #
    #             test: TestEntry
    #             for test in test_list.tests:
    #                 if not test.skip:
    #                     self.run_log.start_test()
    #                     source_path = self.source_path(test.source)
    #                     expected_path, actual_path = self.target_path(test.target)
    #                     param_str = (test.parameters or "").format(outfile=actual_path)
    #                     parms = ([source_path] if source_path else []) + shlex.split(param_str)
    #
    #                     stdout = StringIO()
    #                     stderr = StringIO()
    #                     with redirect_stderr(stderr):
    #                         with redirect_stdout(stdout):
    #                             try:
    #                                 ep(parms, prog_name=module_name)
    #                             except click_tweaker.CLIExitException:
    #                                 pass
    #
    #                     self.evaluate_output(test, stdout.getvalue(), stderr.getvalue(), expected_path, actual_path)
    #                 else:
    #                     self.run_log.log_skipped_test(module_name, test)
    #
    #     print(str(self.run_log))
    #     return self
    #
    #
