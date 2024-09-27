from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from sqlmodel import Session, select
from app.controllers.auth_controllers import generateDecodedToken, generateToken, passwordIntoHash
from app.controllers.users_controllers import  create_user, delete_user_func, get_all_user_func, get_user_by_id_fun, update_user_func, user_login, verify_token
from app.db.db_connectivity import get_session
from app.models.user_models import Create_User, User

router= APIRouter()

blacklisted_tokens: List[str] = []



@router.post("/api/sign_up")
async def sign_up(data:Annotated[dict, Depends(create_user)]):
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="Try again, something occurred while generating token from library. ")
    

@router.post("/api/logIn_user")
async def logIn_user(token: Annotated[dict, Depends(user_login)]):
    if not token:
        HTTPException(
            status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token
        

@router.get("/api/get_all_users")
def get_all_users(users:Annotated[dict, Depends(get_all_user_func)]):
    
    return users

@router.get("/api/get_user")
def get_user(user:Annotated[dict, Depends(get_user_by_id_fun)]):
    return user


@router.put("/api/update_user")
def update_user(updated_user:Annotated[dict, Depends(update_user_func)]):
    print("annelag", updated_user)
    if updated_user:
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="user is not be updated")


# Get Data With Token
@router.get("/api/get_user_with_token")
def get_user_with_token(token:str, session:Annotated[Session, Depends(get_session)]):
    decodede_token= generateDecodedToken(token)
    
    if not decodede_token: 
        raise HTTPException(status_code=404, detail="token has not beed decoded")
    
    user_email = decodede_token["user_email"]
    
    if not user_email:
        raise HTTPException(status_code=404, detail="not find the user email")
    
    db_user = session.exec(select(User).where(User.user_email==user_email)).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not exist") 
    
    return {"user_data" : db_user}



# Signout
@router.delete("/api/sign_out")
def sign_out(token:str, session:Annotated[Session, Depends(get_session)]):
    decodede_token = verify_token(token)
    
    if not decodede_token: 
        raise HTTPException(status_code=404, detail="token has not beed decoded")
    
    user_email = decodede_token["user_email"]
    
    if not user_email:
        raise HTTPException(status_code=404, detail="not find the user email")
    
    db_user = session.exec(select(User).where(User.user_email==user_email)).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not exist") 
    
    # Add the token to the blacklist
    blacklisted_tokens.append(token)

    return {"message": "User signed out successfully"}
    

    
    
# Refresh Token
@router.get("/api/refresh_token")
async def refresh_token(token: str, session: Annotated[Session, Depends(get_session)]):
    decodede_token = verify_token(token)
    if not decodede_token: 
        raise HTTPException(status_code=404, detail="token has not beed decoded")
    
    user_email = decodede_token["user_email"]
    
    if not user_email:
        raise HTTPException(status_code=404, detail="not find the user email")
    
    db_user = session.exec(select(User).where(User.user_email==user_email)).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not exist") 
    
    data= {
        "user_email": db_user.user_email,
        "user_password": db_user.user_password
    }

    # Generate a new access token
    expire_time = timedelta(minutes=30)
    new_access_token = generateToken(data=data, expiry_time= expire_time )

    return {"refresh_access_token": new_access_token}


# Forget Password
@router.get("/forget_password")
def forget_passwords(email: str, session: Annotated[Session, Depends(get_session)]):
    user = session.exec(select(User).where(User.user_email==email)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data= {
        
        "user_password": user.user_password
    }

    # Generate a new access token
    expire_time = timedelta(minutes=30)
    reset_token = generateToken(data=data, expiry_time= expire_time )
   
    return {"access token": reset_token}

# Reset Password
@ router.get("/api/reset_password")
def reset_password(token:str, new_password:str, session:Annotated[Session, Depends(get_session)]):
    decodede_token= generateDecodedToken(token)
    
    if not decodede_token: 
        raise HTTPException(status_code=404, detail="token has not beed decoded")
    
    user_email = decodede_token["user_email"]
    
    if not user_email:
        raise HTTPException(status_code=404, detail="not find the user email")
    
    db_user = session.exec(select(User).where(User.user_email==user_email)).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not exist")
    # convert the new_pasword into hashed
    
    hashed_pasword= passwordIntoHash(new_password)
    
    db_user.user_password = hashed_pasword
    
    session.commit()
    session.refresh(db_user)
    return {"message": "Password reset successfully"}
    

@router.delete("/api/delete_user")
def delete_user(message:Annotated[str, Depends(delete_user_func)]):
    return message