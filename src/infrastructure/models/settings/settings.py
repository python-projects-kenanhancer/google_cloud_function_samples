from pydantic import BaseModel

from . import (
    AirflowCoreSettings,
    AirflowInitSettings,
    BackendDBSettings,
    CdtToNexumSettings,
    DatadogSettings,
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
    datadog: DatadogSettings
