from ruamel.yaml import CommentedMap, CommentedSeq


def add_top_level_spaces(data: CommentedMap | CommentedSeq, count: int = 1):
    if count < 1:
        return

    nl = "\n" * count

    def apply_nl(key):
        data.yaml_set_comment_before_after_key(key, before=nl, indent=0)
        # special case for double-spacing - it's being ignored normally
        if count == 2:
            data.yaml_set_comment_before_after_key(key, before=nl, indent=0)

    if isinstance(data, CommentedMap):
        for key in list(data.keys()):
            apply_nl(key)
    else:
        for i in range(0, len(data)):
            apply_nl(i)
