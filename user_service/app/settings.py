from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta


try:
    config = Config(".env")
    
except:
    config = Config("")
    
    
DATABASE_URL = config("DATABASE_URL", cast=Secret)

expiry_time_str = config.get("ACCESS_EXPIRY_TIME")
access_expiry_time= timedelta(minutes=int(expiry_time_str)) 

admin_expiry_time_str = config.get("ADMIN_EXPIRY_TIME")
admin_access_expiry_time= timedelta(minutes=int(admin_expiry_time_str))


secret_key= config.get("SECRET_KEY")

algorithm= config.get("ALGORITHM")

ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")


