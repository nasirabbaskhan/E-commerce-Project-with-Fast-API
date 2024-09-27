from typing import Annotated, List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.controllers.auth_controllers import generateDecodedToken, generateToken, passwordIntoHash, varifyPassword
from app.db.db_connectivity import DB_Session, get_session
from app.models.user_models import Create_User, Login_User, Update_User, User
from app.settings import access_expiry_time
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.user_producers import get_kafka_producer
from app import user_pb2 
from google.protobuf.json_format import MessageToDict



# In-memory token blacklist
blacklisted_tokens: List[str] = []

# producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
async def create_user(user_form:Create_User, 
                session:Annotated[Session, Depends(get_session)],
                producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    
    # return "hellow kia hall hay"
    
    if not user_form:
        raise HTTPException(status_code=404, detail="user input is incorrect")
    
    # veryfi user is exist
    db_users=session.exec(select(User)).all()
    for user in db_users:
        is_email_exist= user.user_email==user_form.user_email
        is_password_exist= varifyPassword(user_form.user_password, user.user_password)
        
        if (is_email_exist and is_password_exist):
            raise HTTPException(status_code=404, detail="User Email and User Password is already exist")
        elif is_email_exist:
            raise HTTPException(status_code=404, detail="User Email is already exist")
        elif is_password_exist:
            raise HTTPException(status_code=404, detail="User Password is already exist")
        
    # TODO using kafka producer to ading user 
    
    #2: adding the users signup data into database if user's email or password not exist    
    
    # convert the plain password into hashed befor adding into database
    hashedPassword= passwordIntoHash(user_form.user_password)
    
    if not hashedPassword:
        raise HTTPException(status_code=404, detail="user password is not converted int hashed")
    # return user_form
    
    user_proto= user_pb2.User_Proto(user_name=user_form.user_name, user_email=user_form.user_email, phone_number=user_form.phone_number, user_password= hashedPassword)
    print(f"Todo Protobuf: {user_proto}")
    serialized_user=user_proto.SerializeToString()
    print(f"serilized data: {serialized_user}")
    
    try:
        await producer.send_and_wait("user", serialized_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
    
    # Convert Protobuf object to a dictionary
    user_dict = MessageToDict(user_proto)

    return user_dict
    # return user_proto
    # new_user= User(user_name=user_form.user_name,user_email=user_form.user_email, user_password=hashedPassword, phone_number=user_form.phone_number)
    # session.add(new_user)
    # session.commit()
    # session.refresh(new_user)
    # return new_user



def user_login(user_data:Login_User, session:Annotated[Session, Depends(get_session)]):
    db_user=session.exec(select(User).where(User.user_email==user_data.user_email)).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=401, detail=f"User does not exist")
    
    
    is_password_exist= varifyPassword(user_data.user_password, db_user.user_password)
    
    if not is_password_exist:
        raise HTTPException(status_code=404, detail="User password is not exist in data base")
    
    # generate the token
    data= {
        "user_email":user_data.user_email,
        "user_password": user_data.user_password
    }
    token= generateToken(data=data, expiry_time=access_expiry_time)
    
    if token:
        return {"access_token": token, "token_type": "bearer"}
        
    
   
        
def get_all_user_func(sesion:Annotated[Session, Depends(get_session)]):
    users = sesion.exec(select(User)).all()
    
    if not users: 
        raise HTTPException(status_code=404, detail="Users are not exist in database")
    
    return users
                    
def get_user_by_id_fun(user_id:int, session:Annotated[Session, Depends(get_session)]):
    user=session.exec(select(User).where(User.user_id==user_id)).one_or_none()
    
    if not user: 
        raise HTTPException(status_code=404, detail="User is not exist in database")
    
    return user
    
                 
def update_user_func(user_id:int, user_data:Update_User, session:Annotated[Session, Depends(get_session)]):
    db_user= session.exec(select(User).where(User.user_id==user_id)).one_or_none()
  
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not exist")
    
    updated_user= user_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(updated_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    print("inside users",db_user )
    return db_user
               

def delete_user_func(user_id:int, session:Annotated[Session, Depends(get_session)]):
    db_user= session.get(User, user_id)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not existed")
    
    session.delete(db_user)
    session.commit()
    return f"User has been successfully deleted of this id: {user_id}"




# Verify Token
def verify_token(token: str):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    decoded_data = generateDecodedToken(token)
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return decoded_data


def validate_by_id(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user