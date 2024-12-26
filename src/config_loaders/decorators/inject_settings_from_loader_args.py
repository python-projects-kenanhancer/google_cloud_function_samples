from typing import Any, Callable, Type, overload

from config_loaders import ConfigLoaderFactory
from config_loaders.config_loader_args import (
    ConfigLoaderArgs,
    EnvConfigLoaderArgs,
    GcpSecretEnvConfigLoaderArgs,
    GcpSecretJsonConfigLoaderArgs,
    GcpSecretYamlConfigLoaderArgs,
    GcpStorageEnvConfigLoaderArgs,
    GcpStorageJsonConfigLoaderArgs,
    GcpStorageYamlConfigLoaderArgs,
    JsonConfigLoaderArgs,
    YamlConfigLoaderArgs,
)

from .base_inject_settings import TSettings, inject_settings


def load_settings_from_config_loader(*, config_loader_args: ConfigLoaderArgs, SettingsClass: Type[TSettings]):
    env_config_loader = ConfigLoaderFactory.get_loader(config_loader_args=config_loader_args)

    return SettingsClass.load(config_loader=env_config_loader)


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretEnvConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretJsonConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretYamlConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageEnvConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageJsonConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageYamlConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: EnvConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: JsonConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: YamlConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


def inject_settings_from_loader_args(
    config_loader_args: ConfigLoaderArgs, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(load_settings_from_config_loader, param_name=param_name, config_loader_args=config_loader_args)
