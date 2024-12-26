from markupsafe import escape

from schemas import GreetingLanguage, GreetingType

from .greeting_language_decorator import GreetingLanguageDecorator
from .greeting_strategy_factory import GreetingStrategyFactory


class GreetingService:
    def __init__(
        self, greeting_strategy_factory: GreetingStrategyFactory, greeting_type: GreetingType, greeting_language: GreetingLanguage
    ):
        self.greeting_strategy_factory = greeting_strategy_factory
        self.greeting_type = greeting_type
        self.greeting_language = greeting_language

    def get_greeting_message(self, name: str):
        # 1) Create the base greeting strategy (in English)
        greeting_strategy = self.greeting_strategy_factory.create_greeting_strategy(self.greeting_type)

        # 2) Wrap it with the greeting language decorator
        greeting_decorated_strategy = GreetingLanguageDecorator(
            base_greeting_strategy=greeting_strategy, language=self.greeting_language
        )

        # 3) Generate the final prefix
        greeting_prefix = greeting_decorated_strategy.get_greeting_prefix()

        # 4) Combine with the user's name
        return f"{greeting_prefix} {escape(name)}!"
