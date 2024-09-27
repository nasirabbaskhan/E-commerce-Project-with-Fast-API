from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.models.authorizationModel import Admin
from app.db.db_connectivity import get_session
from app.settings import SECRET_KEY, ADMIN_SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")


def admin_required(token: Annotated[str, Depends(oauth2_scheme)], session:Annotated[Session, Depends(get_session)]):
    headers = jwt.get_unverified_headers(token)
    admin_secret = headers.get("secret")
    admin_kid = headers.get("kid")
    payload = decode_jwt(token)
    admin = session.exec(select(Admin).where(Admin.admin_name == payload.get(
        "admin_name")).where(Admin.admin_email == payload.get("admin_email")).where(Admin.admin_kid == admin_kid)).one_or_none()
    print(admin)
    print(admin_secret)

    if not admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not (str(admin_secret) == str(ADMIN_SECRET_KEY)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return payload