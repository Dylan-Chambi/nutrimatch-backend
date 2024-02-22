from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from firebase_admin import auth
from fastapi.security import HTTPAuthorizationCredentials
from firebase_admin.auth import UserRecord

security = HTTPBearer()

async def authentication_jwt_middleware(token: HTTPAuthorizationCredentials = Depends(security)) -> UserRecord:
    try:
        decoded_token = auth.verify_id_token(token.credentials)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

