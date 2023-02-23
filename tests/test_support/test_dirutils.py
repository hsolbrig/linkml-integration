import os.path
import shutil
import unittest

from harness.support.dirutils import make_guarded_directory
from test_support import LOCAL_DATA_DIR


class DirUtilsTestCase(unittest.TestCase):
    """ Test the directory utilities """
    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(LOCAL_DATA_DIR):
            shutil.rmtree(LOCAL_DATA_DIR)

    def test_make_guarded_directory(self):
        # Test the parameter
        with self.assertRaises(ValueError) as e:
            make_guarded_directory(LOCAL_DATA_DIR, '')
        self.assertIn('cannot be empty', str(e.exception))
        path1 = os.path.join('outer_dir', 'middle_dir')
        abs_path1 = os.path.join(LOCAL_DATA_DIR, path1)
        abs_safety_file = os.path.join(abs_path1, 'safety')
        with self.assertRaises(ValueError) as e:
            make_guarded_directory(LOCAL_DATA_DIR, abs_path1)
        self.assertIn('must be relative', str(e.exception))

        # Create the directory and make sure we get exactly one guard file
        make_guarded_directory(LOCAL_DATA_DIR, path1, clear=True)
        self.assertTrue(os.path.exists(abs_path1))
        self.assertTrue(os.path.exists(abs_safety_file))
        self.assertEqual(1, len(os.listdir(abs_path1)))

        # Add a file and a directory and make sure we don't remove it if clear = False
        with open(os.path.join(abs_path1, 'f1.txt'), 'w') as f:
            pass
        make_guarded_directory(abs_path1, 'inner_dir')
        abs_path2 = os.path.join(abs_path1, 'inner_dir')
        make_guarded_directory(LOCAL_DATA_DIR, path1)
        self.assertTrue(os.path.exists(abs_safety_file))
        self.assertEqual(3, len(os.listdir(abs_path1)))
        self.assertTrue(os.path.exists(os.path.join(abs_path2, 'safety')))
        self.assertEqual(1, len(os.listdir(abs_path2)))

        # Make sure things get removed if clear = True
        make_guarded_directory(LOCAL_DATA_DIR, path1, clear=True)
        self.assertTrue(os.path.exists(abs_safety_file))
        self.assertEqual(1, len(os.listdir(abs_path1)))

        # Make sure removal doesn't work if there isn't a safety file
        os.remove(abs_safety_file)
        with self.assertRaises(FileNotFoundError) as e:
            make_guarded_directory(LOCAL_DATA_DIR, path1, clear=True)
        self.assertIn('safety guard file not found', str(e.exception))

    def test_path_list1(self):
        path = os.path.join('outer_dir', 'middle_dir', 'inner_dir')
        abs_path = os.path.join(LOCAL_DATA_DIR, path)
        abs_safety_file = os.path.join(abs_path, 'safety')
        self.assertFalse(os.path.exists(abs_safety_file))
        make_guarded_directory(LOCAL_DATA_DIR, ['outer_dir', 'middle_dir/inner_dir'])
        self.assertTrue(os.path.exists(abs_safety_file))
        make_guarded_directory(LOCAL_DATA_DIR, ['outer_dir/middle_dir', 'inner_dir'], clear=True)
        self.assertTrue(os.path.exists(abs_safety_file))
        with self.assertRaises(ValueError) as e:
            make_guarded_directory(LOCAL_DATA_DIR, ['/outer_dir', 'middle_dir', 'inner_dir'], clear=True)
        self.assertIn('dir_path must be relative to the base', str(e.exception))




if __name__ == '__main__':
    unittest.main()
