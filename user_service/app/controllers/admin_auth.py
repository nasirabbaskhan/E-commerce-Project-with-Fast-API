
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.admin_models import Admin, AdminCreateModel, AdminLoginForm
from app.settings import ADMIN_SECRET_KEY, algorithm, secret_key, admin_access_expiry_time


def create_admin_fun(admin_form:AdminCreateModel, session:Annotated[Session, Depends(get_session)]):
    if not  (admin_form.admin_secret== ADMIN_SECRET_KEY):
        raise HTTPException(status_code=404, detail="ADMIN_SECRET_KEY is not valid")
    admin_exist = session.exec(select(Admin).where(
        Admin.admin_email == admin_form.admin_email)).one_or_none()
    if admin_exist:
        raise HTTPException(status_code=404, detail="Admin is already exist")
    
    admin = Admin(
        admin_name=admin_form.admin_name,
        admin_email=admin_form.admin_email,
        admin_password=admin_form.admin_password,
        admin_secret=admin_form.admin_secret
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


def vrify_admin(admin_data:AdminLoginForm, session:Annotated[Session, Depends(get_session)]):
    if not (admin_data.admin_secret == ADMIN_SECRET_KEY):
        raise HTTPException(status_code=404, detail="You are not admin")
    
    admin = session.exec(select(Admin).where(
        (Admin.admin_email == admin_data.admin_email)
        and (Admin.admin_password == admin_data.admin_password)
    )).one_or_none()

    if not admin:
        HTTPException(status_code=404,
                      detail="Admin not found from this details!")
        
    if admin is not None:
        token = generateToken(admin=admin, admin_secret=admin_data.admin_secret, expires_delta=admin_access_expiry_time)
            
    return {
        "admin_token": token,
        "type": "bearer"
    }    
        
        
        
        
    
    
def generateToken(admin: Admin, admin_secret: str, expires_delta: timedelta) -> str:
    """
    Generate a token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated token.
    """

    # Calculate expiry time
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "admin_name": admin.admin_name,
        "admin_email": admin.admin_email,
        "exp": expire
    }
    headers = {
        "kid": admin.admin_kid,
        "secret": admin_secret,
        "iss": admin.admin_kid
    }

    # Encode token with user data and secret key
    token = jwt.encode(payload, secret_key,
                       algorithm=algorithm, headers=headers)
    return token
