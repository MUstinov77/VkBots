from pydantic import BaseModel


class UserSignupLoginSchema(BaseModel):

    username: str
    password: str


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str