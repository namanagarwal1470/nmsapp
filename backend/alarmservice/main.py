from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.alarm import alarm


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(alarm)





