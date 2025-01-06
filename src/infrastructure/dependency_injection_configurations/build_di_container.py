from typing import Optional

from injector import Injector, Module

from ..config_loaders.config_loader_args import (
    GcpStorageEnvConfigLoaderArgs,
)
from .greeting_module import GreetingModule
from .logging_module import LoggingModule
from .say_hello_settings_module import SayHelloSettingsModule
from .settings_module import SettingsModule


class HookedInjector(Injector):
    def create_object(self, cls, additional_kwargs=None):
        """
        This method is called by Injector any time it needs a new instance of `cls`.
        We create the object normally, then (optionally) wrap it.
        """
        # 1. Let Injector do the normal creation (this includes constructor injection).
        instance = super().create_object(cls, additional_kwargs=additional_kwargs)

        # 2. Decide if we want to wrap this class. Here, we can do a blanket wrap for all,
        #    or only for certain classes. We'll do a blanket wrap in this example.

        #    You might add logic like:
        #    if cls not in (SomeExcludedClass, AnotherClassToSkip):
        #        instance = wrap_methods_in_instance(instance, logging_wrapper)

        # instance = wrap_methods_in_instance(instance, logging_wrapper)
        return instance


def build_di_container(extra_modules: Optional[list[Module]] = None) -> Injector:
    base_modules = [
        LoggingModule(),
        GreetingModule(),
        SettingsModule(
            config_loader_args=GcpStorageEnvConfigLoaderArgs(
                bucket_name="app-config-boilerplate",
                blob_name=".env",
                project_id="nexum-dev-364711",
            )
        ),
        SayHelloSettingsModule(
            GcpStorageEnvConfigLoaderArgs(
                bucket_name="app-config-boilerplate",
                blob_name=".env.say_hello",
                project_id="nexum-dev-364711",
            )
        ),
    ]
    if extra_modules:
        base_modules.extend(extra_modules)

    return HookedInjector(base_modules)
