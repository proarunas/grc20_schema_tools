# just some sanity checks for the value schema
from enum import auto, Enum

from loguru import logger

from validators.validation_helpers.val_error import ValErr, ErrType


class DupeStatus(Enum):
    OK = auto()
    MISSING = auto()
    DUPLICATE = auto()


def val_unique(item, pool) -> DupeStatus:
    if not item:
        return DupeStatus.MISSING
    if item in pool:
        return DupeStatus.DUPLICATE
    pool.add(item)
    return DupeStatus.OK


def validate_value_schema(data: dict) -> list[ValErr]:
    logger.info("Validating Value Schema")
    vtypes = data.get("types", {})

    name_pool = set()
    key_pool = set()
    id_pool = set()
    value_pool = set()

    errors: list[ValErr] = []

    for key, val in vtypes.items():

        def handle_err(ref, missing_err, dupe_err, state):
            if state == DupeStatus.DUPLICATE:
                errors.append(ValErr(dupe_err, [key], f"{ref} is a duplicate"))
            elif state == DupeStatus.MISSING:
                errors.append(ValErr(missing_err, [key], f"{ref} is missing"))

        key_state = val_unique(key, key_pool)
        handle_err("Key", ErrType.UNDEFINED, ErrType.KEY_DUPLICATE, key_state)

        val_state = val_unique(val.get("value"), value_pool)
        handle_err("Value", ErrType.VALUE_MISSING, ErrType.VALUE_DUPLICATE, val_state)

        name_state = val_unique(val.get("name"), name_pool)
        handle_err("Name", ErrType.NAME_MISSING, ErrType.NAME_DUPLICATE, name_state)

        id_state = val_unique(val.get("id"), id_pool)
        handle_err("ID", ErrType.ID_MISSING, ErrType.ID_DUPLICATE, id_state)

    return errors


def validate_and_print(data: dict):
    errors = validate_value_schema(data)
    for error in errors:
        logger.error(error.print())
