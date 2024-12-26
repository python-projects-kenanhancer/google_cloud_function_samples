from typing import Type

from config_loaders import ConfigLoaderFactory, YamlConfigLoaderArgs

from .base_inject_settings import TSettings, inject_settings


def load_settings_from_yaml_file(*, file_path: str, SettingsClass: Type[TSettings]):
    yaml_config_loader = ConfigLoaderFactory.get_loader(YamlConfigLoaderArgs(file_path=file_path))

    return SettingsClass.load(config_loader=yaml_config_loader)


def inject_settings_from_yaml_file(file_path: str, param_name: str = "settings"):
    return inject_settings(load_settings_from_yaml_file, param_name=param_name, file_path=file_path)
