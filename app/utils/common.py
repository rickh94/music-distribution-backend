import uuid

from app.utils.responses import bad_request


def validate_request(body: dict, required_fields: dict):
    """Validate that a request has all required data"""
    for field_key, field_name in required_fields.items():
        if not body.get(field_key):
            return bad_request({"errors": {field_key: f"{field_name} is required."}})
    return None


class MissingValue(Exception):
    pass


def str_uuid():
    return str(uuid.uuid4())
