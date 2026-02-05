from fastapi import FastAPI
from .routes import user_router, post_router, auth_router
from .database import Base, engine
from dotenv import load_dotenv
from .core.exc_handler import register_exception_handlers
import logging



logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Create database tables using async engine on app startup, retrying if DB is not ready
@app.on_event("startup")
async def on_startup():
    import asyncio
    max_retries = 10
    retry_delay = 1  # seconds
    attempt = 0
    while True:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            break
        except Exception as e:
            attempt += 1
            logger.warning(f"Database unavailable (attempt {attempt}/{max_retries}): {e}")
            if attempt >= max_retries:
                logger.error("Max retries reached while waiting for database. Exiting startup.")
                raise
            await asyncio.sleep(retry_delay)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

register_exception_handlers(app)





    
    
    


    
    


    

    