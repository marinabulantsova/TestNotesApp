from api.endpoints.base_api import BaseApi

class AuthApi(BaseApi):
    def register(self, data):
        return self.post("/users/register", data)

    def login(self, data):
        return self.post("/users/login", data)

    def logout(self):
        return self.delete("/users/logout")