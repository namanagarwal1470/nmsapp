from starlette.responses import JSONResponse

from fastapi import APIRouter
from config.db import conn
import requests
from fastapi import HTTPException


config=APIRouter()


@config.get("/getconfig/{boardname}")
async def getconfig(boardname: str | None):
    if not boardname:
        return JSONResponse(content={"message": "boardname not given"}, status_code=400)
    doc = conn.nmsapp.boards.find_one({"name": boardname})

    hardware_service_url = f"http://{doc.get("url")}/getConfig"
    try:
        response = requests.get(hardware_service_url)
        if response.status_code == 200:
            hardware_config = response.json()
            update_result = conn.nmsapp.boards.update_one(
                {"name": boardname},
                {"$set": {"configs": hardware_config}}
            )
            if update_result.modified_count > 0:
                return JSONResponse(content=hardware_config, status_code=200)
            else:
                return JSONResponse(content={"message": "Failed to update the config in the database"}, status_code=500)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch from hardware service")
    except requests.exceptions.RequestException:
        pass

    if doc:
        doc.pop("_id", None)
        return JSONResponse(content=doc.get("configs", {}), status_code=200)
    else:
        return JSONResponse(content={"message": "board is not present"}, status_code=404)






