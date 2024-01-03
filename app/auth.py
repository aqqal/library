from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_KEY = os.getenv("CLIENT_KEY")

bearer_auth = HTTPBearer()  # use token authentication

def validate_token(token: str = Depends(bearer_auth)):
    if token.credentials != CLIENT_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.credentials