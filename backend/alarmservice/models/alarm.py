from pydantic import BaseModel

class Alarm(BaseModel):
    alarmName: str
    alarmDate: str


