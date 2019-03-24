from django.apps import AppConfig

from core.navigation import navigation_controller


class LocalscanConfig(AppConfig):
    name = 'localscan'

    def ready(self):
        navigation_controller.add("Localscan", "localscan:submit")