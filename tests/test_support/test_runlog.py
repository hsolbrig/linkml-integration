import unittest

from harness.run_log import RunLog
from model.python.integration import Module, TestEntry, Filepath, ModuleName, ModuleCallers
from test_support import LOCAL_DATA_DIR


class RunLogTestCase(unittest.TestCase):
    def test_runlog_options(self):
        rl = RunLog(LOCAL_DATA_DIR)
        self.assertIn('Number of tests run: 0', str(rl))
        m = Module('big_tester', 'linkml.generators.csvgen:cli', ModuleCallers.Generator)
        t = TestEntry(Filepath('some/output'))
        rl.start_test(m, t)
        rl.success()
        rl.skipped_module(ModuleName('nogo'))
        rl.skipped_module(Module('nogo_2','linkml.generators.csvgen:cli', ModuleCallers.Generator))
        m = ModuleName('a_module')
        t = TestEntry(name='namedTest', target=Filepath('a/deep/dir', is_directory=True))
        rl.skipped_test(m, t)
        t3 = TestEntry(target=Filepath('a/deep/dir/file.txt'))
        rl.start_test(m, t)
        rl.output_mismatch("A whole bunch'o things\nwent\n\treally wrong")
        t2 = TestEntry(name='namedTest2', target=Filepath('a/deep/dir', is_directory=True))
        rl.start_test(m, t2)
        rl.unexpected_stderr_output("Some text")
        t4 = TestEntry(name='namedTest4', target=Filepath('foo.yaml'))
        rl.start_test(m, t4)
        rl.new_output_file()
        self.assertEqual('''Test Results:
    Skipped modules: 2
    Skipped tests: 1
    Number of tests run: 4
        Success: 1
        New: 1
        Issues: 2''', str(rl).strip())
        self.assertEqual('''Skipped Modules:
	nogo
	nogo_2

Skipped Tests:
	a_module:namedTest

New Files:
	Test: a_module:namedTest4 - File: foo.yaml

Changes:
	Test: big_tester:some/output - File: some/output
	Test: a_module:namedTest - File: a/deep/dir
		A whole bunch'o things
		went
			really wrong
	Test: a_module:namedTest2 - File: a/deep/dir
		Some text
	Test: a_module:namedTest4 - File: foo.yaml''', rl.details().strip())


if __name__ == '__main__':
    unittest.main()
