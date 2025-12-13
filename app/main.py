from fastapi import FastAPI
from .routes import user_router, post_router
from .database import Base, engine
from .models import User
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(post_router)






    
    
    


    
    


    

    