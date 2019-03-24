from django.shortcuts import reverse


class NavigationController(object):
    """
    Handles registration of items in the navigation bar
    """
    apps = []

    def add(self, name, url_name):
        """
        Add an app to the navigation. Note that an "app" in this context refers simply to a tool from
        the users perspective and not necessarily an actual django application. A given django app
        can register zero or more apps.

        name: The name of the app
        url_name: The reverse for the app
        """
        self.apps.append((name, url_name, reverse(url_name)))


navigation_controller = NavigationController()