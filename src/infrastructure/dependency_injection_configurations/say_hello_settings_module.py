from injector import (
    Module,
    provider,
)

from ..config_loaders import ConfigLoaderArgs, load_settings_from_config_loader
from ..models.say_hello_settings import SayHelloSettings


class SayHelloSettingsModule(Module):
    def __init__(self, config_loader_args: ConfigLoaderArgs):
        self.config_loader_args = config_loader_args

    @provider
    def provide_say_hello_settings(self) -> SayHelloSettings:
        say_hello_settings = load_settings_from_config_loader(
            config_loader_args=self.config_loader_args, SettingsClass=SayHelloSettings
        )
        return say_hello_settings
