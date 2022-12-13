from linkml_runtime.loaders import YAMLLoader

from model.integration import Manifest
from testing_source import CONFIG_PATH


def dumpers():
    """ """
    return {k: v for k, v in YAMLLoader().load_any('modules.yaml', Manifest, base_dir=CONFIG_PATH).modules.items()
            if 'dumper_tests' in v.subsets}


if __name__ == '__main__':
    from pprint import pprint
    pprint(dumpers())
