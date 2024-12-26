from dataclasses import dataclass

from schemas import Settings


@dataclass
class UnifiedSettings:
    settings_from_env_file: Settings | None = None
    settings_from_json_file: Settings | None = None
    settings_from_yaml_file: Settings | None = None
    settings_from_env_gcp_secret: Settings | None = None
    settings_from_json_gcp_secret: Settings | None = None
    settings_from_yaml_gcp_secret: Settings | None = None
    settings_from_env_gcp_storage: Settings | None = None
    settings_from_json_gcp_storage: Settings | None = None
    settings_from_yaml_gcp_storage: Settings | None = None
    env_from_gcp_storage: Settings | None = None
    json_from_gcp_storage: Settings | None = None
    yaml_from_gcp_storage: Settings | None = None
