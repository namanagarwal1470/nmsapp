from starlette.responses import JSONResponse

from fastapi import APIRouter
import json

hardware=APIRouter()

CONFIG_FILE_PATH = "routes/config.json"
@hardware.get("/getConfig")
async def getconfig():
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config_data = json.load(file)
        return JSONResponse(content=config_data, status_code=200)

    except FileNotFoundError:
        return JSONResponse(content={"message": "Config file not found"}, status_code=404)
    except json.JSONDecodeError:
        return JSONResponse(content={"message": "Error decoding JSON from file"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)






