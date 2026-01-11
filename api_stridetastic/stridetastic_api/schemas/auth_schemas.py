from ninja import Field, Schema


class LoginSchema(Schema):
    username: str = Field(
        ..., 
        description="Username of the user",
        example="root"
    )
    password: str = Field(
        ...,
        description="Password of the user",
        example="password"
    )

class TokenSchema(Schema):
    access: str = Field(
        ..., 
        description="Access token",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    refresh: str = Field(
        ...,
        description="Refresh token",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )

class RefreshTokenSchema(Schema):
    refresh: str = Field(
        ...,
        description="Refresh token to use for generating a new access token",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )


class UserSchema(Schema):
    id: int = Field(..., description="User id", example=1)
    username: str = Field(..., description="Username", example="guest")
    email: str | None = Field(None, description="Email address", example="guest@example.com")
    is_staff: bool = Field(..., description="User can access privileged features")
    is_superuser: bool = Field(..., description="User is a superuser")
