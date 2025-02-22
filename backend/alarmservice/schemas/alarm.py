def alarmEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "alarmName": item["alarmName"],
        "alarmDate": item["alarmDate"],
    }

def alarmsEntity(items) -> list:
    return [alarmEntity(item) for item in items]



