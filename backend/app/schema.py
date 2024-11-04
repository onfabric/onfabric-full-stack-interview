from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class ApiKeyBase(BaseSchema):
    name: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    id: str
    key: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    last_used_at: Optional[datetime] = None

class PaginatedApiKeys(BaseSchema):
    api_keys: List[ApiKey]
    key_count: int



class UserBase(BaseSchema):
    email: EmailStr
    fullname: Optional[str] = None
    nickname: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    keys: List[ApiKey] = []


# UserRequest schemas
class UserRequestBase(BaseSchema):
    endpoint: str
    method: str
    status_code: int


class UserRequestCreate(UserRequestBase):
    key_id: str


class UserRequest(UserRequestBase):
    id: str
    key_id: str
    created_at: datetime
    updated_at: datetime


class PaginatedUserRequests(BaseSchema):
    requests: List[UserRequest]
    request_count: int