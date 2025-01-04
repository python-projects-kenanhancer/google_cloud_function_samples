from injector import Module, provider, singleton

from ..logger import DatadogLoggerStrategy, LoggerStrategy
from ..models.settings import Settings


class LoggingModule(Module):
    @singleton
    @provider
    def provide_logger_strategy(self, settings: Settings) -> LoggerStrategy:

        datadog = settings.datadog

        return DatadogLoggerStrategy(
            service=datadog.service,
            project_id=datadog.project_id,
            environment=datadog.environment,
            repo_name=datadog.repo_name,
            team=datadog.team,
            log_level=datadog.log_level,
            logger_name=datadog.logger_name,
        )
