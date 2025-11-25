from api.endpoints.base_api import BaseApi

class PasswordApi(BaseApi):
    def forgot_password(self, data):
        return self.post("/users/forgot-password", data=data)

    def verify_reset_token(self, data):
        return self.post("/users/verify-reset-password-token", data=data)

    def reset_password(self, data):
        return self.post("/users/reset-password", data=data)

    def change_password(self, data):
        return self.post("/users/change-password", data=data)
