from ruamel.yaml import CommentedMap


def add_top_level_spaces(data: CommentedMap):
    for key in data.keys():
        data.yaml_set_comment_before_after_key(key, before="\n", indent=0)
