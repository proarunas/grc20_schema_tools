from collections import namedtuple

from loguru import logger
from ruamel.yaml import CommentedSeq, CommentedMap

from yaml_helpers.attributes_helper import PropID, TypeID
from yaml_helpers.yaml_format_helpers import add_top_level_spaces
from yaml_helpers.yaml_io import parse_relation

config = namedtuple("Config", ["key_by_id", "include_id", "include_name", "include_desc"])

c = config(key_by_id=False, include_id=True, include_name=True, include_desc=False)


# c = config(key_by_id=False, include_id=True, include_name=False, include_desc=False)
# c = config(key_by_id=True, include_id=False, include_name=True, include_desc=False)


def _serialize_type_simple(entity: dict, definitions: dict, full_data: dict) -> dict:
    ignored_attrs = []
    if not c.include_name:
        ignored_attrs.append(PropID.NAME)
    if not c.include_desc:
        ignored_attrs.append(PropID.DESC)

    # logger.debug("Serializing: {},\t types: {}",
    #             entity.get(PropID.NAME), ','.join({t.get(PropID.NAME) for t in definitions.values()}))

    attrs, rels = {}, {}
    for type_def in definitions.values():
        for item in type_def.get(PropID.ATTR) or []:
            key, rel = parse_relation(item, full_data)
            if key not in ignored_attrs:
                attrs[key] = rel
        for item in type_def.get(PropID.REL) or []:
            key, rel = parse_relation(item, full_data)
            rels[key] = rel

    result = CommentedMap()
    if c.include_id:
        result["_ID"] = entity.get(PropID.ID)
    result["Types"] = CommentedSeq([t.get(PropID.NAME) for k, t in definitions.items() if k != TypeID.ENTITY])
    result["Types"].fa.set_flow_style()

    # logger.debug(f"available attrs:{attrs}")

    for key, attr in attrs.items():
        # logger.debug(f"Key/attr: {key}:{attr}")
        name = attr.get(PropID.NAME)
        result[name] = entity.get(key, None)

    for key, rel in rels.items():
        r_vals = entity.get(key) or []
        r_vals = [parse_relation(r, full_data) for r in r_vals]
        # logger.debug("     Relation: {}, values: {}", rel[PropID.NAME], r_vals)
        r_vals = [r.get(PropID.NAME) for _, r in r_vals]
        # logger.debug("     Relation: {}, values: {}", rel[PropID.NAME], r_vals)
        if r_vals:
            r_vals = CommentedSeq(r_vals)
            r_vals.fa.set_flow_style()
            result[rel[PropID.NAME]] = r_vals
        else:
            # Make sure that attributes and relations are always present
            if key in [PropID.ATTR, PropID.REL]:
                result[rel[PropID.NAME]] = []

    result.yaml_set_comment_before_after_key('Attributes', before="\n")

    if c.key_by_id:
        key = entity.get(PropID.ID)
    else:
        key = entity.get(PropID.NAME)

    return {key: result}


def generate_basic_summary(data: dict) -> dict:
    if not data:
        raise ValueError("No data to serialize")

    # get the definition for the basic "entity"
    types = data.get(TypeID.TYPE)
    entity_def = {TypeID.ENTITY: types.get(TypeID.ENTITY)}
    logger.debug("Serializing. Got types: {}", len(types))

    # iterate over all base types
    undef_counter, result = 0, CommentedSeq()
    for e_type, entities in data.items():

        # get the definition for the base type
        base_def = {**entity_def, e_type: types.get(e_type)}
        if not base_def:
            raise ValueError(f"Type {e_type} not found")

        # iterate over all entities of each type
        for entity in entities.values():

            # skip entities that are marked to be skipped
            if entity.get(PropID.IGNORE):
                continue

            # get all relevant definitions
            e_def = {**base_def, **{t: types.get(t) for t in (entity.get(PropID.TYPES, []))}}

            # serialize the entity
            result.append(_serialize_type_simple(entity, e_def, data))

    add_top_level_spaces(result, 1)

    return CommentedMap({"Types": result})
