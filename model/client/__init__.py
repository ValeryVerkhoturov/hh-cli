from pydantic import BaseModel


class Client(BaseModel):
    id: int = 1
    client_id: str
    client_secret: str
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
