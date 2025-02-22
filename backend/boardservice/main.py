from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.boardRoutes import *


app = FastAPI()
app.include_router(board)





