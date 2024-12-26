import pytest

from config_loaders import (
    ConfigLoaderFactory,
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
from schemas import Settings
from tests.unit.settings.unified_settings import UnifiedSettings


class TestSettingsWithConfigLoaders:

    @pytest.fixture
    def env_suffix(self, request):
        return request.param

    @pytest.fixture
    def settings(self, env_suffix):

        unified_settings = UnifiedSettings()

        if env_suffix:
            env_suffix = env_suffix.lower()
            env_file = f".env.{env_suffix}"
            json_file = f"config.{env_suffix}.json"
            yaml_file = f"config.{env_suffix}.yaml"
            env_gcp_secret_name = f"app-config-env-{env_suffix}"
            json_gcp_secret_name = f"app-config-json-{env_suffix}"
            yaml_gcp_secret_name = f"app-config-yaml-{env_suffix}"
        else:
            env_file = ".env"
            json_file = "config.json"
            yaml_file = "config.yaml"
            env_gcp_secret_name = "app-config-env"
            json_gcp_secret_name = "app-config-json"
            yaml_gcp_secret_name = "app-config-yaml"

        bucket_name = "app-config-boilerplate"
        project_id = "nexum-dev-364711"

        settings_from_env_file = Settings.load(ConfigLoaderFactory.get_loader(EnvConfigLoaderArgs(file_path=env_file)))
        settings_from_json_file = Settings.load(ConfigLoaderFactory.get_loader(JsonConfigLoaderArgs(file_path=json_file)))
        settings_from_yaml_file = Settings.load(ConfigLoaderFactory.get_loader(YamlConfigLoaderArgs(file_path=yaml_file)))

        settings_from_env_gcp_secret = Settings.load(
            ConfigLoaderFactory.get_loader(GcpSecretEnvConfigLoaderArgs(secret_name=env_gcp_secret_name, project_id=project_id))
        )
        settings_from_json_gcp_secret = Settings.load(
            ConfigLoaderFactory.get_loader(GcpSecretJsonConfigLoaderArgs(secret_name=json_gcp_secret_name, project_id=project_id))
        )
        settings_from_yaml_gcp_secret = Settings.load(
            ConfigLoaderFactory.get_loader(GcpSecretYamlConfigLoaderArgs(secret_name=yaml_gcp_secret_name, project_id=project_id))
        )

        settings_from_env_gcp_storage = Settings.load(
            ConfigLoaderFactory.get_loader(
                GcpStorageEnvConfigLoaderArgs(bucket_name=bucket_name, blob_name=env_file, project_id=project_id)
            )
        )
        settings_from_json_gcp_storage = Settings.load(
            ConfigLoaderFactory.get_loader(
                GcpStorageJsonConfigLoaderArgs(bucket_name=bucket_name, blob_name=json_file, project_id=project_id)
            )
        )
        settings_from_yaml_gcp_storage = Settings.load(
            ConfigLoaderFactory.get_loader(
                GcpStorageYamlConfigLoaderArgs(bucket_name=bucket_name, blob_name=yaml_file, project_id=project_id)
            )
        )

        unified_settings.settings_from_env_file = settings_from_env_file
        unified_settings.settings_from_json_file = settings_from_json_file
        unified_settings.settings_from_yaml_file = settings_from_yaml_file
        unified_settings.settings_from_env_gcp_secret = settings_from_env_gcp_secret
        unified_settings.settings_from_json_gcp_secret = settings_from_json_gcp_secret
        unified_settings.settings_from_yaml_gcp_secret = settings_from_yaml_gcp_secret
        unified_settings.settings_from_env_gcp_storage = settings_from_env_gcp_storage
        unified_settings.settings_from_json_gcp_storage = settings_from_json_gcp_storage
        unified_settings.settings_from_yaml_gcp_storage = settings_from_yaml_gcp_storage

        return unified_settings

    @pytest.mark.parametrize(
        "env_suffix, expected_settings",
        [
            (
                "",
                {
                    "meta_database": {"postgres_user": "airflow", "postgres_db": "airflow"},
                    "airflow_core": {"airflow_uid": 55, "load_examples": False},
                    "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 11},
                },
            ),
            (
                "dev",
                {
                    "meta_database": {"postgres_user": "airflowddddd", "postgres_db": "airflowwwww"},
                    "airflow_core": {"airflow_uid": 0, "load_examples": False},
                    "feature_flags": {"circuit_breaker_enabled": False, "circuit_breaker_duration": -3},
                },
            ),
            (
                "local",
                {
                    "meta_database": {"postgres_user": "KENAN", "postgres_db": "KENAN"},
                    "airflow_core": {"airflow_uid": 1000, "load_examples": True},
                    "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 5},
                },
            ),
        ],
        indirect=["env_suffix"],  # Resolve the `settings` parameter via the fixture
    )
    def test_settings_with_different_environments(self, settings: UnifiedSettings, expected_settings):

        for section, fields in expected_settings.items():
            for field, expected_value in fields.items():
                actual_settings_from_env_file_value = getattr(getattr(settings.settings_from_env_file, section), field)
                actual_settings_from_json_file_value = getattr(getattr(settings.settings_from_json_file, section), field)
                actual_settings_from_yaml_file_value = getattr(getattr(settings.settings_from_yaml_file, section), field)

                actual_settings_from_env_gcp_secret_value = getattr(
                    getattr(settings.settings_from_env_gcp_secret, section), field
                )
                actual_settings_from_json_gcp_secret_value = getattr(
                    getattr(settings.settings_from_json_gcp_secret, section), field
                )
                actual_settings_from_yaml_gcp_secret_value = getattr(
                    getattr(settings.settings_from_yaml_gcp_secret, section), field
                )

                actual_settings_from_env_gcp_storage_value = getattr(
                    getattr(settings.settings_from_env_gcp_storage, section), field
                )
                actual_settings_from_json_gcp_storage_value = getattr(
                    getattr(settings.settings_from_json_gcp_storage, section), field
                )
                actual_settings_from_yaml_gcp_storage_value = getattr(
                    getattr(settings.settings_from_yaml_gcp_storage, section), field
                )

                assert actual_settings_from_env_file_value == expected_value
                assert actual_settings_from_json_file_value == expected_value
                assert actual_settings_from_yaml_file_value == expected_value

                assert actual_settings_from_env_gcp_secret_value == expected_value
                assert actual_settings_from_json_gcp_secret_value == expected_value
                assert actual_settings_from_yaml_gcp_secret_value == expected_value

                assert actual_settings_from_env_gcp_storage_value == expected_value
                assert actual_settings_from_json_gcp_storage_value == expected_value
                assert actual_settings_from_yaml_gcp_storage_value == expected_value
