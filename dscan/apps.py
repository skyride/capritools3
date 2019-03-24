from django.apps import AppConfig

from core.navigation import navigation_controller


class DscanConfig(AppConfig):
    name = 'dscan'

    def ready(self):
        navigation_controller.add("Dscan", "dscan:submit")