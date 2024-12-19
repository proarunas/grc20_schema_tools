from ruamel.yaml import CommentedSeq, CommentedMap

from yaml_helpers.attributes_helper import PropID, TypeID
from yaml_helpers.yaml_format_helpers import add_top_level_spaces
from yaml_helpers.yaml_io import parse_relation


def generate_basic_attribute_summary(data: dict, v_type: dict) -> dict:
    if not data:
        raise ValueError("No data to serialize")

    # Aggregate the attributes
    attributes = {}
    types = data.get(TypeID.TYPE)
    for t in types.values():

        t_name = t.get(PropID.NAME)
        for attrib in t.get(PropID.ATTR) or []:
            key, val = parse_relation(attrib, data)
            if PropID.DESC in val:
                val.pop(PropID.DESC)

            if key in attributes.keys():
                if not t.get(PropID.IGNORE):
                    attributes[key]["_Used In"].append(t_name)
            else:
                val["usage"] = []
                if not t.get(PropID.IGNORE):
                    val["usage"].append(t_name)
                attributes[key] = val

    # generate output
    results = CommentedSeq()
    for key, val in attributes.items():
        name = val.get(PropID.NAME)
        types = [data.get(TypeID.TYPE).get(TypeID.ATTR).get(PropID.NAME)]
        if PropID.TYPES in val:
            types += val.get(PropID.TYPES)
        vt = v_type.get(val.get(PropID.V_TYPE)).get(PropID.NAME)
        attr = CommentedMap({
            "_ID": val.get(PropID.ID),
            "Types": CommentedSeq(types),
            "Name": name,
            "Value Type": vt,
            "_Usage": CommentedSeq(val.get("usage")),
        })
        attr.yaml_set_comment_before_after_key("Value Type", before="\n")
        attr["_Usage"].fa.set_flow_style()
        attr["Types"].fa.set_flow_style()
        results.append({name: attr})

    add_top_level_spaces(results, 1)
    return CommentedMap({"Attributes": results})
