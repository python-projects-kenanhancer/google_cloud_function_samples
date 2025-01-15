import time

from infrastructure import LoggerStrategy

from ..decorators import Context, Next


def time_middleware(context: Context, next: Next, logger: LoggerStrategy):

    start = time.time()
    logger.info("[TIME] Start timing...")
    result = next()
    elapsed = time.time() - start
    logger.info(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result
