from ninja_extra import api_controller, route
from django.contrib.auth import authenticate
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from ..schemas.common_schemas import MessageSchema
from ..schemas.auth_schemas import (
    LoginSchema,
    TokenSchema,
    RefreshTokenSchema,
    UserSchema,
)

auth = JWTAuth()

@api_controller('/auth', tags=['Authentication'], permissions=[])
class AuthController:
    @route.post("/login", response={
        200: TokenSchema,
        401: MessageSchema
    })
    def login(self, data: LoginSchema):
        """
        Handle user login.
        """
        user = authenticate(username=data.username, password=data.password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
        
            return 200, TokenSchema(access=str(access), refresh=str(refresh))
        return 401, MessageSchema(message="Invalid credentials")


    @route.post("/refresh-token", response={
        200: TokenSchema,
        401: MessageSchema
    })
    def refresh_token(self, data: RefreshTokenSchema):
        """
        Handle token refresh.
        """
        try:
            refresh = RefreshToken(data.refresh)
            access = refresh.access_token
            
            return 200, TokenSchema(access=str(access), refresh=str(refresh))
        except Exception as e:
            return 401, MessageSchema(message="Invalid refresh token")

    @route.get("/me", response={200: UserSchema, 401: MessageSchema}, auth=auth)
    def me(self, request):
        """
        Return the authenticated user's profile.
        """
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return 401, MessageSchema(message="Not authenticated")
        return 200, UserSchema(
            id=user.id,
            username=user.username,
            email=user.email or None,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
        
        
