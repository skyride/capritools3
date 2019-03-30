import requests


class ESI(object):
    url = "https://esi.evetech.net"

    def get(self, path, **kwargs):
        return requests.get(self.url+path, **kwargs)

    def post(self, path, **kwargs):
        return requests.post(self.url+path, **kwargs)

    def put(self, path, **kwargs):
        return requests.put(self.url+path, **kwargs)

    def get(self, path, **kwargs):
        return requests.delete(self.url+path, **kwargs)