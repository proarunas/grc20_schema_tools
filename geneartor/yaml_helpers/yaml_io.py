import os

from loguru import logger
from ruamel.yaml import YAMLError, CommentedMap, StringIO

from yaml_helpers.attributes_helper import PropID
from yaml_helpers.yaml_setup import yaml


def load_data(path: str) -> dict | None:
    logger.debug("Loading data...")
    with open(path) as file:
        try:
            data = yaml.load(file)
            logger.debug("   Loading successful.")
            _flatten_all(data)
            return data

        except YAMLError as error:
            logger.error("Error loading schema: {}", error)
            return None


def _flatten_item(data: dict):
    if PropID.EXPAND not in data:
        return

    # generate key order
    keys = list(data.keys())
    r_index = keys.index(PropID.EXPAND)
    keys = keys[:r_index] + list(data[PropID.EXPAND].keys()) + keys[r_index + 1:]

    # basic flatten
    data.update(data.pop(PropID.EXPAND))

    # reorder pairs -  inefficient, but good enough for now
    new_data = CommentedMap()
    for key in keys:
        new_data[key] = data[key]
    data.clear()
    data.update(new_data)


def _flatten_all(data: dict):
    if isinstance(data, dict):
        _flatten_item(data)
        for value in data.values():
            _flatten_all(value)
    elif isinstance(data, list):
        for item in data:
            _flatten_all(item)


def find_entity(full_data: dict, e_type: str, e_key: str):
    return full_data.get(e_type, {}).get(e_key)


def parse_relation(item: dict | str, full_data: dict) -> (str, dict):
    if isinstance(item, dict):
        key, value = next(iter(item.items()))
        return key, value
    elif isinstance(item, str):
        r_type, key = item.split(".")
        entity = find_entity(full_data, r_type, key)
        if not entity:
            raise ValueError(f"Entity {r_type}.{key} not found")
        return key, entity
    else:
        raise ValueError(f"Invalid attribute definition: {item}")


def to_yaml_str(data: dict) -> str:
    output = StringIO()
    yaml.dump(data, output)
    return output.getvalue()


def to_yaml_file(data: dict, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        yaml.dump(data, file)
