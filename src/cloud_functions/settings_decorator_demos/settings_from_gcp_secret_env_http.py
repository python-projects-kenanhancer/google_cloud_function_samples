import functions_framework
from flask import Request, Response, make_response

from config_loaders import inject_settings_from_gcp_secret_env
from schemas import Settings


@functions_framework.http
@inject_settings_from_gcp_secret_env(secret_name="app-config-env", project_id="nexum-dev-364711")
def settings_from_gcp_secret_env_http(request: Request, settings: Settings) -> Response:

    if settings.feature_flags.circuit_breaker_enabled:
        response = make_response((f"Circuit Breaker is enabled", 200))
    else:
        response = make_response((f"Environment variable sql_alchemy_conn={settings.backend_db.sql_alchemy_conn}", 200))

    return response
