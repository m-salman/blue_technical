import os
import yaml
import logging

logger = logging.getLogger(__name__)

default = 'docker'
env = os.environ.get('ENV', default)


def replace_config_env(env, default_config):
    for key, value in default_config.items():
        default_config[key] = value.replace('{{env}}', env) if type(value) is str else value

    return default_config

def _load_config_from_file(env):
    with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as file:
        try:
            configuration = yaml.load(file)
            config = replace_config_env(env, configuration[default])
            config.update(configuration[env])
            return config
        except yaml.YAMLError:
            logger.exception('Failed to load config from file')
            return None


config = _load_config_from_file(env)



