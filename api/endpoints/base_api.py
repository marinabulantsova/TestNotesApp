import requests

class BaseApi:
    def __init__(self, base_url, token = None):
        self.base_url = base_url
        self.session = requests.Session()
        if token:
            self.session.headers.update({"x-auth-token": token})

    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params)

    def post(self, endpoint, data=None):
        return self.session.post(f"{self.base_url}{endpoint}", data=data)

    def put(self, endpoint, data=None):
        return self.session.put(f"{self.base_url}{endpoint}", data=data)

    def patch(self, endpoint, data=None):
        return self.session.patch(f"{self.base_url}{endpoint}", data=data)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}")