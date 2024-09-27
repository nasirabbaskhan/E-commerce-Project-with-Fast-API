from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta


try:
    config = Config(".env")
    
except:
    config = Config("")
    
    
DATABASE_URL = config("DATABASE_URL", cast=Secret)



admin_expiry_time_str = config.get("ADMIN_EXPIRY_TIME")
admin_access_expiry_time= timedelta(minutes=int(admin_expiry_time_str))


ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")


SECRET_KEY = config.get("SECRET_KEY")