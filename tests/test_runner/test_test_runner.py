import os
import unittest

from harness.harness import Harness
from harness.runner import HarnessRunner
from model.python.integration import SubsetName
from . import CONFIGS, INPUTS, EXPECTEDS, ACTUALS


class RunnerTestCase(unittest.TestCase):
    def test_help_file_run(self):
        """ Test a basic help file emitter """
        harness = Harness(os.path.join(CONFIGS, 'help_config.yaml'))
        if harness.has_errors() or harness.has_warnings():
            print()
            print(harness.details())
            self.fail("Test harness configuration error")
        runner = HarnessRunner(harness, INPUTS, os.path.join(EXPECTEDS, 'help_files'), os.path.join(ACTUALS, 'help_files'))
        runner.run()
        self.assertEqual(1, runner._n)
        print(str(runner.run_log))
        self.assertEqual(True, False)

    def test_runner_setup(self):
        harness = Harness(CONFIGS)
        runner = HarnessRunner(harness, INPUTS, EXPECTEDS, ACTUALS, only_subsets=[SubsetName('subset_a')])
        runner.only_modules.append('yaml_loader')
        runner.only_subsets.append('subset_a')
        runner.only_tests.append('First Test')
        runner.exclude_modules.append('yaml_loader')
        runner.exclude_subsets.append('subset_b')
        runner.run()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
