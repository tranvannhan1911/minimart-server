class ApiCode():
    def toDict(code, message, data=None):
        return {
            "code": code,
            "message": message,
            "data": data
        }

    def success(code=1, message="success", data=None):
        return ApiCode.toDict(code, message, data)

    def error(code=0, message="error", data=None):
        return ApiCode.toDict(code, message, data)

