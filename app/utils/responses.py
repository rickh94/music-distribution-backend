import ujson


def success(body, status_code=200):
    return build_response(status_code, body)


def failure(body, status_code=500):
    return build_response(status_code, body)


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": ujson.dumps(body),
    }


def not_found():
    return build_response(404, "Could not find matching item")


def bad_request(message):
    return build_response(400, message)


def something_has_gone_wrong():
    return build_response(500, "Something has gone wrong")


def data_or_404(res_data):
    if not res_data:
        return not_found()
    return success(res_data)


def validation_error(body):
    return {
        "statusCode": 422,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": body,
    }
