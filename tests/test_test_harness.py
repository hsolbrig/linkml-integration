import os
import unittest
from typing import List, Optional

from harness_source.harness import Harness
from harness_source import CONFIG_PATH
from tests import DATA_DIR


class HarnessTestCase(unittest.TestCase):
    def _check_messages(self, h: Harness, expected_warnings: List[str], expected_errors: List[str]) -> None:
        def _check_list(expected: List[str], actual: List[str], typ: str) -> str:
            """ Check whether msgs more or less contain expected """
            not_found = expected.copy()
            not_expected = []   # Actual, not expected
            for a in actual:
                found = False
                for e in not_found:
                    if e in a:
                        not_found.remove(e)
                        found = True
                        break
                if not found:
                    not_expected.append(a)
            rval = ""
            if not_found:
                rval += f"Missing expected {typ} messages:\n\t" + "\n\t".join(not_found) + '\n'
            if not_expected:
                rval += f"Unexpected {typ} messages:\n\t" + "\n\t".join(not_expected) + '\n\n'
            return rval

        rval = _check_list(expected_warnings, h.configuration_warnings, "warning")
        rval += _check_list(expected_errors, h.configuration_errors, "error")
        if rval:
            self.fail(msg=rval)

    def test_basic_load_function(self):
        """ Test a basic (passing) nested load """
        h = Harness(os.path.join(DATA_DIR, 'conf'))
        self._check_messages(h, [], [])

    def test_empty_directory(self):
        h = Harness(os.path.join(DATA_DIR, 'conf_w_errors', 'empty_directory'))
        self._check_messages(h, [], ["No valid configuration files"])

    def test_various_errors(self):
        """ Test the various sorts of errors that might be encountered """
        h = Harness(os.path.join(DATA_DIR, 'conf_w_errors', 'bad_references'))
        self._check_messages(h,
                             ["Module yaml_loader_e: Unrecognized subset: subset_x"],
                             ["Unrecognized entry point: harness_source.support.basic_comparatorsz:string_comparator",
                              "Unrecognized method: identity_filter_e in entry_point: harness_source.support.filters:identity_filter_e",
                              "Module yaml_loader_e: Unrecognized comparator: string_comparatorx",
                              "Module yaml_loader_e: Unrecognized filter: string_comparatorx",
                              "Testing module yaml_loader is not defined"])

    def test_real_config_file(self):
        """ Make sure the official integration config files work """
        h = Harness(CONFIG_PATH)
        self._check_messages(h, [], [])


if __name__ == '__main__':
    unittest.main()
