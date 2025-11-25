from api.endpoints.base_api import BaseApi

class ProfileApi(BaseApi):
    def get_profile(self):
        return self.get("/users/profile")

    def update_profile(self, data):
        return self.patch("/users/profile", data=data)

    def delete_profile(self):
        return self.delete("/users/delete-account")
