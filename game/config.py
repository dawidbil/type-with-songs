import sys
import os.path
import yaml
from dotmap import DotMap
from game.utils import get_project_base_path


class Config:
    def __init__(self):
        try:
            with open(os.path.join(get_project_base_path(), 'config.yaml'), 'r') as file:
                config_file = yaml.safe_load(file)
        except FileNotFoundError:
            print("No 'config.yaml' file in the project root directory")
            sys.exit(1)
        except yaml.YAMLError as exception:
            print(f"Error when opening config: {exception}")
            sys.exit(1)

        if not isinstance(config_file, dict):
            raise ValueError("config.yaml top level structure should be a dict")

        self.dotmap = DotMap(config_file)

    def __getattr__(self, item):
        return self.dotmap.get(item)

    # only for auto completion in editor
    def __dir__(self):
        return self.dotmap.__dir__()


sys.modules[__name__] = Config()
