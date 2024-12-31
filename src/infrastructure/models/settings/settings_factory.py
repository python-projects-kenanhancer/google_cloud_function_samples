from infrastructure import ConfigLoaderArgs, ConfigLoaderFactory

from . import Settings


class SettingsFactory:

    @classmethod
    def load(cls, config_loader_args: ConfigLoaderArgs) -> Settings:
        config_loader = ConfigLoaderFactory.get_loader(config_loader_args)
        raw_config = config_loader.load()
        return Settings(**raw_config)
