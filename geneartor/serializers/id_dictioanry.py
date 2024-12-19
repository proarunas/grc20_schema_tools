from ruamel.yaml import CommentedMap, CommentedSeq

from yaml_helpers.attributes_helper import PropID, TypeID
from yaml_helpers.yaml_format_helpers import add_top_level_spaces
from yaml_helpers.yaml_io import parse_relation


def generate_id_dict(data: dict) -> CommentedMap:
    result = CommentedSeq()

    # get the type names from the schema
    types = data.get(TypeID.TYPE)
    type_name = types.get(TypeID.TYPE).get(PropID.NAME)
    attr_name = types.get(TypeID.ATTR).get(PropID.NAME)
    rel_name = types.get(TypeID.REL).get(PropID.NAME)

    # set up the id dictionaries
    id_list = CommentedSeq()
    result.append({type_name: id_list})
    attr_list = CommentedSeq()
    result.append({attr_name: attr_list})
    rel_list = CommentedSeq()
    result.append({rel_name: rel_list})

    # iterate over all types
    for e_type, entities in data.items():
        if entities is None:
            continue

        t_name = types.get(e_type).get(PropID.NAME)

        sub_l = None
        for item in result:
            if t_name in item:
                sub_l = item[t_name]
                break

        if sub_l is None:
            sub_l = CommentedSeq()
            result.append({t_name: sub_l})

        for key, entity in entities.items():
            # skip ignored entities
            if entity.get(PropID.IGNORE):
                continue

            # store the entity id
            sub_l.append({entity.get(PropID.NAME): entity.get(PropID.ID)})

            # handle attributes
            for item in entity.get(PropID.ATTR) or []:
                key, rel = parse_relation(item, data)
                attr_list.append({rel.get(PropID.NAME): rel.get(PropID.ID)})

            # handle relations
            for item in entity.get(PropID.REL) or []:
                key, rel = parse_relation(item, data)
                rel_list.append({rel.get(PropID.NAME): rel.get(PropID.ID)})


    add_top_level_spaces(result)

    return CommentedMap({"Simple ID Dictionary": result})
