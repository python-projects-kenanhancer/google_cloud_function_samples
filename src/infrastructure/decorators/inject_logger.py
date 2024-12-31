import functools
import logging
import threading
from typing import Any, Callable

# Global lock and flag to ensure we configure logging only once
_config_lock = threading.Lock()
_global_logger_configured = False


def _configure_logging_globally():
    """
    Configures the logger once globally.
    Subsequent calls do nothing.
    """
    global _global_logger_configured
    if not _global_logger_configured:
        with _config_lock:
            # Double check inside the lock to avoid race conditions
            if not _global_logger_configured:
                logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                )
                _global_logger_configured = True


def inject_logger(logger_name: str | None = None):
    """
    A decorator that:
      1) Ensures the global logger is configured exactly once.
      2) Injects a 'logger' keyword argument into the wrapped function.

    If 'logger' is not provided in kwargs, it creates one using either:
      - the provided 'logger_name', or
      - the function's module name (e.g., 'my_package.my_module') if logger_name is None.

    Usage:
        @inject_logger()
        def my_func(arg, logger=None):
            logger.info("Hello from my_func, arg=%s", arg)

        # You can also specify a custom logger name:
        @inject_logger(logger_name="special_logger")
        def another_func(x, logger=None):
            logger.warning("Something interesting happened, x=%s", x)
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1) Configure logging globally only once
            _configure_logging_globally()

            # 2) Inject a logger if not provided
            if "logger" not in kwargs:
                name = logger_name or func.__module__  # e.g. 'my_package.my_module'
                kwargs["logger"] = logging.getLogger(name)

            return func(*args, **kwargs)

        return wrapper

    return decorator
