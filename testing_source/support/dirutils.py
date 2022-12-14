import os
import shutil

from testing_source import BASE_DIR, OUTPUT_BASE


def make_testing_directory(directory: str, clear: bool = False) -> None:
    """
    Create directory if necessary and clear it if requested
    :param directory: Directory to create
    :param clear: True means remove everything there
    """
    if clear or not os.path.exists(directory):
        safety_file = os.path.join(directory, "generated")
        if os.path.exists(directory):
            if not os.path.exists(safety_file):
                raise FileNotFoundError(
                    f"'generated' guard file not found in {directory}"
                )
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
        with open(safety_file, "w") as f:
            f.write(
                "Generated for safety.  Directory will not be cleared if this file is not present"
            )


def make_output_directory_for(fname: str, is_directory: bool) -> None:
    """
    Make a directory for fname
    :param fname: File name to make the directory for
    :param is_directory: True means fname is a directory name, false, a file name
    """
    if not is_directory:
        make_output_directory_for(os.path.dirname(fname), True)
    else:
        if not os.path.relpath(fname, OUTPUT_BASE).startswith('.'):
            make_output_directory_for(os.path.dirname(fname), True)
            make_testing_directory(fname)

