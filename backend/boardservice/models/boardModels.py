from pydantic import BaseModel

class Board(BaseModel):
    name: str | None
    type: str | None
    configs: str | None
    url: str | None
    circle: str |None
    sapid: str | None
    version: str |None
    state: str| None
    alarms : str| None




