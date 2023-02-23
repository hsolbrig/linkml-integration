from dataclasses import dataclass, field
from time import time
from typing import List, Union, Dict, Optional

from harness.support.test_id import TestID
from model.python.integration import Module, TestEntry, ModuleName

@dataclass
class TestResult:
    expected_output_file: str
    start_timestamp: float = field(default_factory=time)
    end_timestamp: float = None
    success: bool = None
    new_test: bool = None
    fail_reason: List[str] = field(default_factory=list)
    addl_info: List[str] = field(default_factory=list)


class RunLog:

    def __init__(self, expected_base_dir: str):
        self.test_record: Dict[str, TestResult] = dict()
        self.skipped_modules: List[ModuleName] = []
        self.skipped_tests: List[TestID] = []
        self.config_errors: List[str] = []
        self.output_base_dir = expected_base_dir
        self.active_test: Optional[TestResult] = None
        self.active_test_name: Optional[str] = None

    def start_test(self, module: Union[Module, ModuleName], test_entry: TestEntry) -> None:
        assert self.active_test_name is None, f"Last test: {self.active_test_name} did not terminate correctly"
        self.active_test_name = str(TestID(module, test_entry))
        self.active_test = TestResult(test_entry.target.path)

    def end_test(self, final_return: bool) -> bool:
        self.active_test.end_timestamp = time()
        self.test_record[self.active_test_name] = self.active_test
        self.active_test_name = None
        self.active_test = None
        return final_return

    def skipped_module(self, module: Union[Module, ModuleName]):
        self.skipped_modules.append(module.name if isinstance(module, Module) else module)

    def skipped_test(self, module: Union[Module, ModuleName], test: TestEntry):
        self.skipped_tests.append(TestID(module, test))

    def success(self) -> bool:
        """ Log success and return continue testing indicator """
        self.active_test.success = True
        return self.end_test(True)

    def output_mismatch(self, compare_result: Union[str, List[str]]) -> bool:
        """
        The actual output of the test doesn't match the expected output
        :param compare_result: description of the difference
        :return: False
        """
        self.active_test.success = False
        self.active_test.fail_reason += \
            compare_result if isinstance(compare_result, list) else compare_result.split('\n')
        return self.end_test(False)

    def new_output_file(self) -> bool:
        """ Log the addition of a new test to the output """
        self.active_test.success = False
        self.active_test.new_test = True
        return self.end_test(True)

    def config_error(self, text: str):
        self.config_errors.append(text)

    def unexpected_stderr_output(self, text: Union[str, List[str]]) -> bool:
        self.active_test.success = False
        self.active_test.addl_info = text if isinstance(text, list) else text.split('\n')
        return self.end_test(False)

    def _n_success(self) -> int:
        return sum([1 if tr.success else 0 for tr in self.test_record.values()])

    def _n_new(self):
        return sum([1 if tr.new_test else 0 for tr in self.test_record.values()])

    def _n_issues(self):
        return sum([1 if not tr.new_test and not tr.success else 0 for tr in self.test_record.values()])

    def _n_tests(self):
        return len(self.test_record)

    def __str__(self):
        return f"""Test Results:
    Skipped modules: {len(self.skipped_modules)}
    Skipped tests: {len(self.skipped_tests)}
    Number of tests run: {self._n_tests()}
        Success: {self._n_success()}
        New: {self._n_new()}
        Issues: {self._n_issues()}"""

    def details(self) -> str:
        rval: List[str] = []
        if len(self.skipped_modules):
            rval.append("")
            rval.append("Skipped Modules:")
            for sm in self.skipped_modules:
                rval.append(f"\t{sm}")
        if len(self.skipped_tests):
            rval.append("")
            rval.append("Skipped Tests:")
            for st in self.skipped_tests:
                rval.append(f"\t{st}")
        if self._n_new():
            rval.append("")
            rval.append("New Files:")
            for k, nf in self.test_record.items():
                if nf.new_test:
                    rval.append(f"\tTest: {k} - File: {nf.expected_output_file}")
        if self._n_issues():
            rval.append("")
            rval.append("Changes:")
            for k, cf in self.test_record.items():
                rval.append(f"\tTest: {k} - File: {cf.expected_output_file}")
                if cf.fail_reason:
                    rval.append("\t\t" + "\n\t\t".join(cf.fail_reason))
                if cf.addl_info:
                    rval.append("\t\t" + "\n\t\t".join(cf.addl_info))
        return '\n' + '\n'.join(rval)


