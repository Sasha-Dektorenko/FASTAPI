from dotenv import load_dotenv
import os

load_dotenv()  

DB_URL = os.getenv("DB_URL", "sqlite:///./database.db")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRES_TIME = int(os.getenv("EXPIRES_TIME", 30))*60