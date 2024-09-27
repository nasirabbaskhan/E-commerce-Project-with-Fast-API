from passlib.context import CryptContext # type: ignore
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.settings import access_expiry_time, algorithm, secret_key





def generateToken(data:dict, expiry_time:timedelta):
    try:
        to_encoded_data= data.copy()
        
        to_encoded_data.update({
            "exp": datetime.utcnow() + expiry_time
            # "exp": datetime.utcnow() + access_expiry_time
        })
        
        acces_token = jwt.encode(to_encoded_data, secret_key, algorithm = algorithm)
        return acces_token
    except JWTError as je:
        print("JWT error", je)
        return je

def generateDecodedToken(token):
    try:
        decodeToken = jwt.decode(token, secret_key, algorithms = algorithm)
        return decodeToken 
    except JWTError as je:
        print("JWT Error", je)
        return je




pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def passwordIntoHash(password:str):
    hashed_password=pwd_context.hash(password)
    return hashed_password
    


def varifyPassword(plainText:str, hashedPassword:str):
    return pwd_context.verify(plainText, hashedPassword)
    