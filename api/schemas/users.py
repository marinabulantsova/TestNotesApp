from pydantic import EmailStr
from typing import Optional
from api.schemas.base import BaseResponse, BaseModel

class UserRegister(BaseModel):
    id: str
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    id: str
    email: EmailStr
    name: str
    token: str

class UserData(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None

class UserRegisterResponse(BaseResponse):
    data: UserRegister

class UserLoginResponse(BaseModel):
    data: UserLogin

class UserDataResponse(BaseModel):
    data: UserData