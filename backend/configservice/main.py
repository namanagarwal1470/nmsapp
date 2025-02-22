from fastapi import FastAPI
from routes.route import config


app = FastAPI()
app.include_router(config)





