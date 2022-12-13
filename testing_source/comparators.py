from linkml_runtime.loaders import YAMLLoader

from model.integration import Manifest
from testing_source import CONFIG_PATH


def comparators():
    """ """
    return YAMLLoader().load_any('comparators.yaml', Manifest, base_dir=CONFIG_PATH).comparators


if __name__ == '__main__':
    from pprint import pprint
    pprint(comparators())
