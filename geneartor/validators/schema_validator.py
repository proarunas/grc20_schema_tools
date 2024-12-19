from loguru import logger

from validators.validation_helpers.val_error import ErrType, ValErr
from yaml_helpers.attributes_helper import TypeID, PropID
from validators.validation_helpers.id_handler import validate_id


def add_error(errors: list[ValErr], error_type: ErrType, entity_path: list[str], message: str):
    # logger.debug(f"Error: {error_type} in {entity_path}: {message}")
    errors.append(ValErr(error_type, entity_path, message))


def validate(data: dict) -> list[ValErr]:
    logger.info("Validating schema")
    types = data.get(TypeID.TYPE, {})
    type_list = list(types.keys())

    id_pool = set()
    key_pools: dict[str, set] = {}
    attr_key_pool = key_pools.setdefault(TypeID.ATTR, set())
    rel_key_pool = key_pools.setdefault(TypeID.REL, set())

    errors: list[ValErr] = []

    # validate top level to start with
    for e_type, entities in data.items():

        if entities is None:
            continue

        if e_type not in type_list:
            add_error(errors, ErrType.TYPE_INVALID, [e_type], "Entity type is not defined")

        type_pool = key_pools.setdefault(e_type, set())

        for e_key, entity in entities.items():
            # logger.debug(f"Validating: {e_type} - {key}")
            # logger.debug("    ID pool: {}", id_pool)

            if entity.get(PropID.IGNORE):
                continue

            # validate the key
            if e_key in type_pool:
                add_error(errors, ErrType.KEY_DUPLICATE, [e_type, e_key], "Duplicate Entity `key`: " + e_key)
            type_pool.add(e_key)

            if not entity.get(PropID.NAME):
                add_error(errors, ErrType.NAME_MISSING, [e_type, e_key], "Missing Entity `name`")

            # validate the id
            e_id = entity.get(PropID.ID)
            if not e_id:
                add_error(errors, ErrType.ID_MISSING, [e_type, e_key], "Missing Entity `id`")
            else:
                if e_id in id_pool:
                    add_error(errors, ErrType.ID_DUPLICATE, [e_type, e_key], "Duplicate Entity `id`: " + e_id)
                else:
                    id_pool.add(e_id)

                valid, error = validate_id(e_id)
                if not valid:
                    add_error(errors, ErrType.ID_INVALID, [e_type, e_key], error)

            # ---- validate attributes

            for item in entity.get(PropID.ATTR) or []:
                # not following references
                if not isinstance(item, dict):
                    continue

                a_key, rel = next(iter(item.items()))
                if a_key in attr_key_pool:
                    add_error(errors, ErrType.KEY_DUPLICATE, [e_type, e_key, a_key],
                              "Duplicate Attribute `key`: " + a_key)
                else:
                    attr_key_pool.add(a_key)

                att_name = rel.get(PropID.NAME)
                if not att_name:
                    add_error(errors, ErrType.NAME_MISSING, [e_type, e_key, a_key], "Missing Attribute `name`")

                att_id = rel.get(PropID.ID)
                # logger.debug(f"    Attribute: {key} - {att_id}")
                if not att_id:
                    add_error(errors, ErrType.ID_MISSING, [e_type, e_key, a_key], "Missing Attribute `id`")
                elif att_id in id_pool:
                    add_error(errors, ErrType.ID_DUPLICATE, [e_type, e_key, a_key],
                              f"Duplicate Attribute `id`: {att_id}")
                else:
                    id_pool.add(att_id)

            for item in entity.get(PropID.REL) or []:
                if not isinstance(item, dict):
                    continue

                r_key, rel = next(iter(item.items()))
                if r_key in rel_key_pool:
                    add_error(errors, ErrType.KEY_DUPLICATE, [e_type, e_key, r_key],
                              "Duplicate Relation `key`: " + r_key)
                else:
                    rel_key_pool.add(r_key)

                rel_name = rel.get(PropID.NAME)
                if not rel_name:
                    add_error(errors, ErrType.NAME_MISSING, [e_type, e_key, r_key], "Missing Relation `name`")

                rel_id = rel.get(PropID.ID)
                if not rel_id:
                    add_error(errors, ErrType.ID_MISSING, [e_type, e_key, r_key], "Missing Relation `id`")
                elif rel_id in id_pool:
                    add_error(errors, ErrType.ID_DUPLICATE, [e_type, e_key, r_key],
                              f"Duplicate Relation `id`: {rel_id}")
                else:
                    id_pool.add(rel_id)

            # TODO validate:
            # - check that attributes are defined in types
            # - check that relations are defined in types

    return errors
