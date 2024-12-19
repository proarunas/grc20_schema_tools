from ruamel.yaml import CommentedMap, CommentedSeq


def apply_nl(data, keys, count):
    for key in keys:
        data.yaml_set_comment_before_after_key(key, before="\n" * count, indent=0)
        # special case for double-spacing - it's being ignored normally
        if count == 2:
            data.yaml_set_comment_before_after_key(key, before="\n", indent=0)


def add_top_level_spaces(data: CommentedMap | CommentedSeq, count: int = 1):
    if count < 1:
        return

    if isinstance(data, CommentedMap):
        keys = list(data.keys())
    else:
        keys = range(0, len(data))

    apply_nl(data, keys, count)
