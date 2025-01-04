import requests

from ..logger_strategy import LoggerStrategy


class DatadogApiLoggerStrategy(LoggerStrategy):
    def __init__(
        self,
        api_key: str,
        service: str = "my_python_app_test",
        environment: str = "dev",
        hostname: str = "localhost",
        region: str = "us",
    ):
        self.api_key = api_key
        self.service = service
        self.env = environment
        self.hostname = hostname
        self.region = region.lower()

        """
        US default endpoint:
            https://http-intake.logs.datadoghq.com/v1/input
        EU endpoint:
            https://http-intake.logs.datadoghq.eu/v1/input
        """
        if self.region == "eu":
            self.logs_endpoint = "https://http-intake.logs.datadoghq.eu/v1/input"
        else:
            self.logs_endpoint = "https://http-intake.logs.datadoghq.com/v1/input"

    def _send_log(self, level: str, message: str):
        payload = {
            "message": message,
            "ddsource": "python",
            "service": self.service,
            "hostname": self.hostname,
            "ddtags": f"env:{self.env},level:{level}",
            # "ddtags": f"service:{self.service},environment:{self.env},project_id:{project_id},repo_name:{repo_name},team:cdt"
        }

        # ddtags = f"service:{service},environment:{environment},project_id:{project_id},repo_name:{repo_name},team:cdt"
        # endpoint = f"https://http-intake.logs.datadoghq.com/api/v2/logs?dd-api-key={get_datadog_api_key()}&ddtags={ddtags}&ddsource={service}&service={service}"

        headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
        }

        response = requests.post(self.logs_endpoint, headers=headers, json=payload)
        # Hata durumunda exception fırlatabilir veya sadece loglayabilirsiniz
        response.raise_for_status()

    def info(self, msg: str, *args, **kwargs) -> None:
        formatted_msg = msg % args if args else msg
        self._send_log("info", formatted_msg)

    def warning(self, msg: str, *args, **kwargs) -> None:
        formatted_msg = msg % args if args else msg
        self._send_log("warning", formatted_msg)

    def error(self, msg: str, *args, **kwargs) -> None:
        formatted_msg = msg % args if args else msg
        self._send_log("error", formatted_msg)

    def debug(self, msg: str, *args, **kwargs) -> None:
        formatted_msg = msg % args if args else msg
        self._send_log("debug", formatted_msg)
