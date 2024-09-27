
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.controllers.admin_auth import create_admin_fun, vrify_admin
from app.db.db_connectivity import get_session


router= APIRouter()


@router.post("/api/create_admin")
def create_admin(admin:Annotated[dict, Depends(create_admin_fun)]):
    if not admin:
        raise HTTPException(status_code=404, detail="Admin has not created successfully!")
    return admin


@router.post("/api/admin_login")
def admin_login(token:Annotated[dict, Depends(vrify_admin)]):
    if not token:
        raise HTTPException(status_code=404, detail="Admin has not verified!")
    return token