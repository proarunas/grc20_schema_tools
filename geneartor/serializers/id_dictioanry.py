from ruamel.yaml import CommentedMap

from yaml_helpers.attributes_helper import PropID, TypeID
from yaml_helpers.yaml_format_helpers import add_top_level_spaces
from yaml_helpers.yaml_io import parse_relation


def generate_id_dict(data: dict) -> dict:
    id_dict = CommentedMap()

    # get the type names from the schema
    types = data.get(TypeID.TYPE)
    type_name = types.get(TypeID.TYPE).get(PropID.NAME)
    attr_name = types.get(TypeID.ATTR).get(PropID.NAME)
    rel_name = types.get(TypeID.REL).get(PropID.NAME)

    # set up the id dictionaries
    id_dict.setdefault(type_name, {})
    attr_dict = id_dict.setdefault(attr_name, {})
    rel_dict = id_dict.setdefault(rel_name, {})

    # iterate over all types
    for e_type, entities in data.items():
        if entities is None:
            continue

        t_name = types.get(e_type).get(PropID.NAME)
        sub_d = id_dict.setdefault(t_name, {})

        for key, entity in entities.items():
            # skip ignored entities
            if entity.get(PropID.IGNORE):
                continue

            # store the entity id
            sub_d[entity.get(PropID.NAME)] = entity.get(PropID.ID)

            # handle attributes
            for item in entity.get(PropID.ATTR) or []:
                key, rel = parse_relation(item, data)
                attr_dict[rel.get(PropID.NAME)] = rel.get(PropID.ID)

            # handle relations
            for item in entity.get(PropID.REL) or []:
                key, rel = parse_relation(item, data)
                rel_dict[rel.get(PropID.NAME)] = rel.get(PropID.ID)

        # just in case all entities are ignored
        if not sub_d:
            del id_dict[e_type]

    add_top_level_spaces(id_dict)

    return id_dict
