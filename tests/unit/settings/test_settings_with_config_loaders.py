import pytest
from injector import Injector

from domain import GreetingLanguage, GreetingType
from infrastructure import DatadogSettings, GcpStorageEnvConfigLoaderArgs, Settings, SettingsModule


class TestSettingsWithConfigLoaders:

    @pytest.fixture
    def settings(self) -> Settings:

        env_file = ".env.say_hello"

        bucket_name = "app-config-boilerplate"
        project_id = "nexum-dev-364711"

        injector = Injector(
            [SettingsModule(GcpStorageEnvConfigLoaderArgs(bucket_name=bucket_name, blob_name=env_file, project_id=project_id))]
        )

        settings_from_env_gcp_storage = injector.get(Settings)

        return settings_from_env_gcp_storage

    @pytest.fixture
    def expected_settings(self) -> Settings:

        return Settings(
            default_name="World",
            greeting_type=GreetingType.TIME_BASED,
            greeting_language=GreetingLanguage.EN,
            datadog=DatadogSettings(
                service="ovo_cdt_to_nexum",
                environment="dev",
                project_id="nexum-dev-364711",
                repo_name="cdt_dags",
                team="cdt",
                log_level="info",
                logger_name="info",
            ),
        )

    def test_settings_with_different_environments(self, settings: Settings, expected_settings: Settings):
        assert settings.to_dict() == expected_settings.to_dict()
