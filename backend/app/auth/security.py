from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models.user import User

# Use passlib CryptContext with multiple schemes:
# - prefer bcrypt for new hashes (stronger and standard for production)
# - keep pbkdf2_sha256 as a fallback so existing hashes still verify during migration
# Note: bcrypt may require a binary dependency on some systems; CI/dev may fallback to
# pbkdf2_sha256 if bcrypt isn't available. Passlib will verify and re-hash on next login
# if you implement re-hash logic.
# Detect whether a working bcrypt backend is available at runtime. Some environments
# (CI or Windows with a problematic `bcrypt` wheel) may have an installed but
# non-functional bcrypt module which causes runtime errors; in that case we fall
# back to using pbkdf2_sha256 only to keep the app/test-suite working.
try:
    import bcrypt as _bcrypt_mod  # type: ignore
    try:
        # quick smoke test to ensure bcrypt can hash
        _bcrypt_mod.hashpw(b"test", _bcrypt_mod.gensalt())
        _bcrypt_available = True
    except Exception:
        _bcrypt_available = False
except Exception:
    _bcrypt_available = False

if _bcrypt_available:
    # choose default based on settings; fall back to pbkdf2 if preferred isn't available
    preferred = getattr(settings, "preferred_password_scheme", "pbkdf2_sha256")
    if preferred == "bcrypt":
        default_scheme = "bcrypt"
    else:
        default_scheme = "pbkdf2_sha256"
    pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], default=default_scheme, deprecated="auto")
else:
    logging.warning("bcrypt backend unavailable or broken; falling back to pbkdf2_sha256 for password hashing")
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # the token 'sub' may be a string; ensure it's an int for DB lookup
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def needs_rehash(hashed_password: str) -> bool:
    """Return True if the given hash should be updated to the current preferred scheme.

    This wraps Passlib's `needs_update` API so callers (e.g. the login route) can
    decide to re-hash and persist a stronger hash transparently on next successful login.
    """
    try:
        return pwd_context.needs_update(hashed_password)
    except Exception:
        # If anything goes wrong, don't force a rehash (avoid locking users out)
        return False
