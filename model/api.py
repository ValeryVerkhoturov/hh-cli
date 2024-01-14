from pydantic import BaseModel


class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
