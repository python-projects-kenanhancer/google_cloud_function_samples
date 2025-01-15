from infrastructure import LoggerStrategy

from ..decorators import Context, Next


def logger_middleware(context: Context, next: Next, logger: LoggerStrategy):

    logger.info(f"[LOGGER] About to call {context.func.__name__}" f" with args={context.args}, kwargs={context.kwargs}")
    result = next()
    logger.info(f"[LOGGER] Finished {context.func.__name__}, result={result}")
    return result
