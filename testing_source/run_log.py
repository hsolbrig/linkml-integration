import os.path
from dataclasses import dataclass
from typing import List, Optional, Tuple

from model.integration import Module, TestEntry, ModuleName
from testing_source import BASE_DIR


class RunLog:
    @dataclass
    class TestID:
        module: Module
        test: TestEntry

    @dataclass
    class TestResult:
        test: "RunLog.TestID"
        expected_fname: str
        compare_output: Optional[str] = None

        def __post_init__(self):
            self.expected_fname = os.path.relpath(self.expected_fname, BASE_DIR)

    def __init__(self):
        self.new_output_files: List["RunLog.TestResult"] = []
        self.output_changes: List["RunLog.TestResult"] = []
        self.skipped_modules: List[ModuleName] = []
        self.skipped_tests: List[Tuple[ModuleName, str]] = []
        self.ntests: int = 0
        self.nsuccess: int = 0

    def start_test(self) -> None:
        self.ntests += 1

    def log_skipped_module(self, module: Module):
        self.skipped_modules.append(module.name)

    def log_skipped_test(self, module: Module, test: TestEntry):
        self.skipped_tests.append((module.name, test.target))

    def log_success(self, module: Module, test:TestEntry) -> bool:
        """ Log success and return continue testing indicator """
        self.nsuccess += 1
        return True

    def log_file_mismatch(self, module: Module, test:TestEntry, expected_fn: str, compare_result: str) -> bool:
        self.output_changes.append(RunLog.TestResult(RunLog.TestID(module, test), expected_fn, compare_result))
        return True

    def log_new_test(self, module: Module, test:TestEntry, expected_fn: str) -> bool:
        """ Log the addition of a new test to the output """
        self.new_output_files.append(RunLog.TestResult(RunLog.TestID(module, test), expected_fn))
        return True

    def __str__(self):
        return f"""Test Results:
    Skipped modules: {len(self.skipped_modules)}
    Skipped tests: {len(self.skipped_tests)}
    Number of tests: {self.ntests}
    Passes: {self.nsuccess}
    New: {len(self.new_output_files)}
    Mismatches: {len(self.output_changes)}"""
