import functools
import ujson

import pydantic
import pynamodb.exceptions

from app.utils.common import MissingValue
from app.utils.responses import (
    something_has_gone_wrong,
    bad_request,
    not_found,
    validation_error,
)


class MissingID(Exception):
    pass


def something_might_go_wrong(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pynamodb.exceptions.DoesNotExist as err:
            print(err)
            return not_found()
        except pydantic.ValidationError as err:
            return validation_error(err.json())
        except MissingValue as err:
            print(err)
            return validation_error(ujson.dumps(str(err)))
        except MissingID as err:
            print(err)
            return bad_request("ID is required in path")
        except Exception as err:
            print(err)
            return something_has_gone_wrong()

    return wrapper


def load_and_validate(
    required_fields: dict, *, with_identity: bool = False, with_path_id: bool = False
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            data = ujson.loads(event["body"])
            for field_key, field_name in required_fields.items():
                if not data.get(field_key):
                    return bad_request(
                        {"errors": {field_key: f"{field_name} is required."}}
                    )
            kwargs = {}
            if with_identity:
                kwargs["identity_id"] = event["requestContext"]["identity"][
                    "cognitoIdentityId"
                ]
            if with_path_id:
                try:
                    kwargs["path_id"] = event["pathParameters"]["id"]
                except KeyError:
                    kwargs["path_id"] = None
            return func(data, **kwargs)

        return wrapper

    return decorator


def load_model(
    model, *, with_identity: bool = False, with_path_id: bool = False,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            data = ujson.loads(event["body"])
            item = model(**data)
            kwargs = {}
            if with_identity:
                kwargs["identity_id"] = event["requestContext"]["identity"][
                    "cognitoIdentityId"
                ]
            if with_path_id:
                try:
                    kwargs["path_id"] = event["pathParameters"]["id"]
                except KeyError:
                    raise MissingID("ID is required in path.")
            return func(item, **kwargs)

        return wrapper

    return decorator


def get_todo_ids(func):
    @functools.wraps(func)
    def wrapper(event, _context):
        try:
            todo_id = event["pathParameters"]["id"]
            user_id = event["requestContext"]["identity"]["cognitoIdentityId"]
        except KeyError:
            return bad_request("User id and todo id are required")
        return func(user_id, todo_id, event)

    return wrapper


def get_id_from_path(func):
    @functools.wraps(func)
    def wrapper(event, _context):
        try:
            return func(id_=event["pathParameters"]["id"])
        except KeyError:
            return bad_request("ID is required in URL.")

    return wrapper


def no_args(func):
    @functools.wraps(func)
    def wrapper(*_):
        return func()

    return wrapper
