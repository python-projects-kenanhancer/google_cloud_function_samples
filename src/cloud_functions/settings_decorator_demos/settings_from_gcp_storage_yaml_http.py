import functions_framework
from flask import Request, Response, make_response

from config_loaders import inject_settings_from_gcp_storage_yaml
from models import Settings


@functions_framework.http
@inject_settings_from_gcp_storage_yaml(
    bucket_name="app-config-boilerplate", blob_name="config.yaml", project_id="nexum-dev-364711"
)
def settings_from_gcp_storage_yaml_http(request: Request, settings: Settings) -> Response:

    if settings.feature_flags.circuit_breaker_enabled:
        response = make_response((f"Circuit Breaker is enabled", 200))
    else:
        response = make_response((f"Environment variable sql_alchemy_conn={settings.backend_db.sql_alchemy_conn}", 200))

    return response
