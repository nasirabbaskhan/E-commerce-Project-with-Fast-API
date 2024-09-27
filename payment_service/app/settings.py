from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta


try:
    config = Config(".env")
    
except:
    config = Config("")
    
    
DATABASE_URL = config("DATABASE_URL", cast=Secret)



