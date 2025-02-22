from starlette.responses import JSONResponse

from models.boardModels import *
from fastapi import APIRouter
from config.db import conn
from fastapi import FastAPI,Request

board=APIRouter()


@board.get("/board/read/{boardname}",response_model=Board)
async def getboarddetails(boardname: str | None):
    if boardname:
        doc=conn.nmsapp.boards.find_one({"name" : boardname})
        if doc:
            doc.pop("_id",None)
            return JSONResponse(content=doc,status_code=200)
        else:
            return JSONResponse(content={"message": "board is not present"},status_code=404)

    return JSONResponse(content={"message": "boardname not given"})


@board.get("/board/get/{boardtype}")
async def getallBoardsUsingType(boardtype : str | None):
    if boardtype:
        docs = conn.nmsapp.boards.find({"type": boardtype})
        board_details = []

        for doc in docs:
            doc.pop("_id", None)
            board_details.append(doc)

        if board_details:
            return JSONResponse(content=board_details, status_code=200)
        else:
            return JSONResponse(content={"message": "No boards found for this type"}, status_code=404)

    return JSONResponse(content={"message": "boardtype not given"}, status_code=400)

@board.get("/board/get/{boardcircle}")
async def getallBoardsUsingCircle(boardcircle : str | None):
    if boardcircle:
        docs = conn.nmsapp.boards.find({"circle": boardcircle})
        board_details = []

        for doc in docs:
            doc.pop("_id", None)
            board_details.append(doc)

        if board_details:
            return JSONResponse(content=board_details, status_code=200)
        else:
            return JSONResponse(content={"message": "No boards found for this circle"}, status_code=404)

    return JSONResponse(content={"message": "boardcircle not given"}, status_code=400)

@board.post("/board/create")
async def addboard(request: Board):
    request=dict(request)
    existing_board = conn.nmsapp.boards.find_one({"name": request["name"]})
    if existing_board:
        return  JSONResponse(content={"message": "board is already present "}, status_code=400)

    conn.nmsapp.boards.insert_one(request)
    return  JSONResponse(content={"message": "board is added"}, status_code=200)

@board.delete("/board/delete/{boardname}")
async def deleteboard(boardname: str | None):
    if boardname:
        doc=conn.nmsapp.boards.find_one({"name" : boardname})
        if doc:
            conn.nmsapp.boards.delete_one({"name": boardname})
            return JSONResponse(content={"message": "board deleted"},status_code=200)
        else:
            return JSONResponse(content={"message": "board is not present"},status_code=404)

    return JSONResponse(content={"message": "boardname not given"})



