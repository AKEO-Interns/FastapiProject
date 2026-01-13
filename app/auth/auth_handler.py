

from datetime import datetime, timedelta, timezone
import hashlib

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.appConfig import Settings
from app.core.context import current_user_ctx


class AuthService:
    def __init__(self):
        self.SECRET_KEY = Settings.SECRET_KEY
        self.ALGORITHM = Settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES

        if not self.SECRET_KEY or not self.ALGORITHM:
            raise RuntimeError("JWT env variables missing")

        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

        self.security = HTTPBearer()

    # -------- PASSWORD HANDLING --------
    @staticmethod
    def _normalize_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(
            self._normalize_password(password)
        )

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.pwd_context.verify(
            self._normalize_password(password),
            hashed
        )

    # -------- JWT HANDLING --------
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> str:
        token = credentials.credentials
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            user_id = int(payload.get("sub"))
         
           
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
                
            user_id = int(user_id)
            current_user_ctx.set(user_id)
            print( "get current user for list:",current_user_ctx.get())
            return user_id

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def verify_jwt_token(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            return True
        except JWTError:
            return False
        
auth = AuthService()       
