from ruamel.yaml import CommentedMap, CommentedSeq


def add_top_level_spaces(data: CommentedMap | CommentedSeq):
    if isinstance(data, CommentedMap):
        for key in list(data.keys())[1:]:
            data.yaml_set_comment_before_after_key(key, before="\n", indent=0)
    else:
        for i in range(1,len(data)):
            data.yaml_set_comment_before_after_key(i, before="\n", indent=0)
