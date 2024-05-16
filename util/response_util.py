def success(data=None):
    return {"code": 1, "data": data}


def ok(msg):
    return {"code": 1, "msg": msg}


def fail(msg=None):
    return {"code": 0, "msg": msg}


def result(code, msg, data):
    return {"code": code, "msg": msg, "data": data}
