from linkml_runtime.loaders import YAMLLoader

from model.integration import Manifest
from testing_source import CONFIG_PATH


def subsets():
    """ """
    return YAMLLoader().load_any('subsets.yaml', Manifest, base_dir=CONFIG_PATH).subsets


if __name__ == '__main__':
    from pprint import pprint
    pprint(subsets())
