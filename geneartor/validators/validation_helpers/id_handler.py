import uuid

import base58


def is_base58(s: str) -> bool:
    try:
        base58.b58decode(s)
        return True
    except ValueError:
        return False


def validate_id_or_null(geo_id: str) -> (bool, str):
    if geo_id is None:
        return True, ""

    return validate_id(geo_id)


def validate_id(geo_id: str) -> (bool, str):
    if not isinstance(geo_id, str):
        return False, "ID is not a string"

    if len(geo_id) != 22:
        return False, f"ID is not the correct length. Expected: 22, Got: {len(geo_id)}"

    if not is_base58(geo_id):
        return False, "ID is not base58"

    return True, ""


def generate_id() -> str:
    return base58.b58encode(uuid.uuid4().bytes).decode('utf-8')
