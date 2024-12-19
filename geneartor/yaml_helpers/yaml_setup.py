from ruamel.yaml import YAML


def _represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '~')


def _setup_yaml():
    new_yaml = YAML()
    new_yaml.representer.add_representer(type(None), _represent_none)

    # yaml config
    new_yaml.indent(mapping=2, sequence=4, offset=2)
    new_yaml.width = 80
    new_yaml.default_flow_style = False
    new_yaml.explicit_start = True
    new_yaml.explicit_end = True
    new_yaml.allow_unicode = True

    return new_yaml


yaml = _setup_yaml()


