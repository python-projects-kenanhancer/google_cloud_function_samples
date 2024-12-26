from pydantic import BaseModel

from config_loaders import ConfigLoader
from schemas.settings import (
    AirflowCoreSettings,
    AirflowInitSettings,
    BackendDBSettings,
    CdtToNexumSettings,
    Environment,
    FeatureFlagsSettings,
    MetaDatabaseSettings,
)


class Settings(BaseModel):
    project_env: Environment

    feature_flags: FeatureFlagsSettings
    meta_database: MetaDatabaseSettings
    backend_db: BackendDBSettings
    airflow_init: AirflowInitSettings
    airflow_core: AirflowCoreSettings
    cdt_to_nexum: CdtToNexumSettings

    @classmethod
    def load(cls, config_loader: ConfigLoader) -> "Settings":
        config = config_loader.load()
        return cls(**config)
