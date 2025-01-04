from typing import Optional

from injector import Injector, Module

from domain import GreetingModule

from ..config_loaders.config_loader_args import (
    GcpStorageEnvConfigLoaderArgs,
)
from .logging_module import LoggingModule
from .say_hello_settings_module import SayHelloSettingsModule
from .settings_module import SettingsModule


def build_di_container(extra_modules: Optional[list[Module]] = None) -> Injector:
    base_modules = [
        LoggingModule(),
        GreetingModule(),
        SettingsModule(
            config_loader_args=GcpStorageEnvConfigLoaderArgs(
                bucket_name="app-config-boilerplate",
                blob_name=".env",
                project_id="nexum-dev-364711",
            )
        ),
        SayHelloSettingsModule(
            GcpStorageEnvConfigLoaderArgs(
                bucket_name="app-config-boilerplate",
                blob_name=".env.say_hello",
                project_id="nexum-dev-364711",
            )
        ),
    ]
    if extra_modules:
        base_modules.extend(extra_modules)

    return Injector(base_modules)
