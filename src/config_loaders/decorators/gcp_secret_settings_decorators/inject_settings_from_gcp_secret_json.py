from typing import Any, Callable, Type

from config_loaders import ConfigLoaderFactory, GcpSecretJsonConfigLoaderArgs

from ..base_inject_settings import TSettings, inject_settings


def load_settings_from_gcp_secret_json(*, secret_name: str, project_id: str, SettingsClass: Type[TSettings]) -> TSettings:
    gcp_json_config_loader = ConfigLoaderFactory.get_loader(
        GcpSecretJsonConfigLoaderArgs(secret_name=secret_name, project_id=project_id)
    )
    return SettingsClass.load(config_loader=gcp_json_config_loader)


def inject_settings_from_gcp_secret_json(
    secret_name: str, project_id: str, param_name: str = "settings"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(
        load_settings_from_gcp_secret_json, param_name=param_name, secret_name=secret_name, project_id=project_id
    )
