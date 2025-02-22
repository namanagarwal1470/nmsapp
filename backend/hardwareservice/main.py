from fastapi import FastAPI
from routes.route import hardware


app = FastAPI()
app.include_router(hardware)





