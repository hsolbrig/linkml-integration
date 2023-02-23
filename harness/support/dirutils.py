import filecmp
import os
import shutil
from contextlib import redirect_stdout
from io import StringIO
from typing import Optional, Union, List

from harness.support.filters import ldcontext_metadata_filter


def make_guarded_directory(base: str, dir_path: Union[str, List[str]], *, clear: bool = False) -> None:
    """
    Create a nested set of directories relative to base adding guard files as needed
    :param base: base directory - directory is built relative to this
    :param dir_path: subdirectory path(s) relative to the base
    :param clear: True means clear everything except the guard files in the leaf directory
    """
    def make_safety_file() -> None:
        os.makedirs(abs_dir, exist_ok=True)
        if not os.path.exists(safety_file):
            with open(safety_file, "w") as f:
                f.write("Generated for safety.  Directory will not be cleared if this file is not present")

    # iterate downwards creating and/or clearing subdirectories
    if not dir_path:
        raise ValueError("dir_path cannot be empty")
    dir_path = dir_path if isinstance(dir_path, str) else os.path.join(*dir_path)
    if os.path.isabs(dir_path):
        raise ValueError("dir_path must be relative to the base")

    abs_dir = os.path.join(base, dir_path)
    safety_file = os.path.join(abs_dir, "safety")
    if clear and os.path.exists(abs_dir):
        if not os.path.exists(safety_file):
            raise FileNotFoundError(f"safety guard file not found in {dir_path}")
        shutil.rmtree(abs_dir)
    make_safety_file()


class dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """

    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(
            self.left, self.right, self.common_files, shallow=False
        )
        self.same_files, self.diff_files, self.funny_files = fcomp

    filecmp.dircmp.methodmap["same_files"] = phase3
    filecmp.dircmp.methodmap["diff_files"] = phase3
    filecmp.dircmp.methodmap["funny_files"] = phase3


def _do_cmp(f1, f2):
    bufsize = filecmp.BUFSIZE
    with open(f1, "rb") as fp1, open(f2, "rb") as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if f1.endswith(".context.jsonld"):
                b1 = ldcontext_metadata_filter(b1.decode())
                b2 = ldcontext_metadata_filter(b2.decode())
            if b1 != b2:
                return False
            if not b1:
                return True


filecmp._do_cmp = _do_cmp


def directory_comparator(dir1: str, dir2: str) -> Optional[str]:
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: None if directories match, else summary of differences
    """

    def has_local_diffs(dc: dircmp) -> bool:
        return bool(dc.diff_files or dc.funny_files or dc.left_only or dc.right_only)

    def has_diffs(dc: dircmp) -> bool:
        return has_local_diffs(dc) or any(has_diffs(sd) for sd in dc.subdirs.values())

    dirs_cmp = dircmp(dir1, dir2, ignore=["generated"])
    if has_diffs(dirs_cmp):
        output = StringIO()
        with redirect_stdout(output):
            dirs_cmp.report_full_closure()
        return output.getvalue()
    return None
