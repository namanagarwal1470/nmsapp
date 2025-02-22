from models.alarm import Alarm
from fastapi import APIRouter
from config.db import conn
from schemas.alarm import alarmEntity,alarmsEntity
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

alarm=APIRouter()
templates=Jinja2Templates(directory="templates")

@alarm.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs=conn.nmsapp.alarm.find({})
    newDocs=alarmsEntity(docs)
    return templates.TemplateResponse(
        "index.html" ,{"request": request,"newDocs":newDocs}
    )


@alarm.post("/add")
async def add_note(request: Request):
    form=await request.form()
    print(form)
    formdict=dict(form)
    conn.nmsapp.alarm.insert_one(formdict)
    docs=conn.nmsapp.alarm.find({})
    newDocs=alarmsEntity(docs)
    return templates.TemplateResponse(
        "index1.html" ,{"request": request,"newDocs":newDocs}
    )

