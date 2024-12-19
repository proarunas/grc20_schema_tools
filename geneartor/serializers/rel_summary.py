from collections import namedtuple

from ruamel.yaml import CommentedMap, CommentedSeq

from yaml_helpers.attributes_helper import PropID, TypeID
from yaml_helpers.yaml_format_helpers import add_top_level_spaces
from yaml_helpers.yaml_io import parse_relation

config = namedtuple("Config", ["key_by_id", "include_id", "include_name", "include_desc"])


def generate_basic_relation_summary(data: dict) -> dict:
    if not data:
        raise ValueError("No data to serialize")

    # Aggregate the attributes
    rels = {}
    types = data.get(TypeID.TYPE)
    for t in types.values():

        t_name = t.get(PropID.NAME)
        for attrib in t.get(PropID.REL) or []:
            key, val = parse_relation(attrib, data)
            if PropID.DESC in val:
                val.pop(PropID.DESC)

            if key in rels.keys():
                if not t.get(PropID.IGNORE):
                    rels[key]["_Used In"].append(t_name)
            else:
                val["usage"] = []
                if not t.get(PropID.IGNORE):
                    val["usage"].append(t_name)
                rels[key] = val


    # generate output
    results = CommentedSeq()
    for key, val in rels.items():
         name = val.get(PropID.NAME)
         types = [data.get(TypeID.TYPE).get(TypeID.REL).get(PropID.NAME)]
         if PropID.TYPES in val:
             types += val.get(PropID.TYPES)
         rl_names = []
         for rl in val.get(PropID.R_LIMIT):
             rl_type, rl_entity = rl.split(".")
             rl_names.append(data.get(rl_type).get(rl_entity).get(PropID.NAME))

         attr = CommentedMap({
             "_ID": val.get(PropID.ID),
             "Types": CommentedSeq(types),
             "Name": name,
             "Relation value types": CommentedSeq(rl_names),
             "_Usage": CommentedSeq(val.get("usage")),
         })
         attr.yaml_set_comment_before_after_key("Relation value types", before="\n")
         attr["_Usage"].fa.set_flow_style()
         attr["Types"].fa.set_flow_style()
         attr["Relation value types"].fa.set_flow_style()
         results.append({name: attr})

    add_top_level_spaces(results, 1)
    return CommentedMap({"Relation Types": results})
