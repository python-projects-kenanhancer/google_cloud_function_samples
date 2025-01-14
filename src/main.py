from infrastructure import (
    LoggerStrategy,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
)
from interfaces.cli.commands import GreetingCommand
from interfaces.dtos import GreetingCliArgs

# Parameter Object Design Pattern
# Result Object Design Pattern


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    time_middleware,
)
def main(args: GreetingCliArgs, greeting_command: GreetingCommand, logger: LoggerStrategy):

    try:
        # Execute command
        greeting_command.execute(first_name="kenan", last_name="hancer", args=args)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
