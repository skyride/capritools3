from django.apps import AppConfig

from core.navigation import navigation_controller


class PastebinConfig(AppConfig):
    name = 'pastebin'

    def ready(self):
        navigation_controller.add("Pastebin", "pastebin:submit")