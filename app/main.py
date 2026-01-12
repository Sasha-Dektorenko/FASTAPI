from fastapi import FastAPI
from .routes import user_router, post_router, auth_router
from .database import Base, engine
from dotenv import load_dotenv
from .core.exc_handler import register_exception_handlers
import logging



logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

register_exception_handlers(app)





    
    
    


    
    


    

    