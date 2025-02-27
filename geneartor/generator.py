import os
import sys

from loguru import logger

from serializers.attr_summary import generate_basic_attribute_summary
from serializers.id_dictioanry import generate_id_dict
from serializers.rel_summary import generate_basic_relation_summary
from serializers.type_summary import generate_basic_summary
from validators.schema_validator import validate
from validators.validation_helpers.val_error import ValErr, ErrType
from validators.value_type_validator import validate_value_schema
from yaml_helpers.yaml_io import load_data, to_yaml_file

schema_dir = "../schema/"
main_schema_path = os.path.join(schema_dir, "base_schema.yaml")
value_types_path = os.path.join(schema_dir, "value_types.yaml")

output_dir = "../generated/"
summary_file_path = os.path.join(output_dir, "type_summary.yaml")
attribute_summary_path = os.path.join(output_dir, "attribute_summary.yaml")
rel_summary_path = os.path.join(output_dir, "relation_summary.yaml")
id_dict_file_path = os.path.join(output_dir, "id_dict.yaml")

debug = False

if not debug:
    logger.remove()
    logger.add(sys.stderr, level="INFO")


def print_errors(errors: list[ValErr]):
    for error in errors:
        if error.error_type == ErrType.ID_MISSING:
            logger.warning(error.print())
        else:
            logger.error(error.print())


def load_schema() -> (dict, dict):
    logger.info("Loading and validating `Base Schema` from: {}", main_schema_path)
    schema = load_data(main_schema_path)
    print_errors(validate(schema))

    logger.info("Loading and validating `Value Types` from: {}", value_types_path)
    v_types = load_data(value_types_path)
    print_errors(validate_value_schema(v_types))

    return schema, v_types.get("v_type")


def generate_basics(schema: dict, v_types: dict):
    logger.info("Generating ID Dictionary")
    id_dict = generate_id_dict(schema)
    to_yaml_file(id_dict, id_dict_file_path)
    logger.success("ID Dictionary Generated at: {}", id_dict_file_path)

    logger.info("Generating Type Summary")
    summary = generate_basic_summary(schema)
    to_yaml_file(summary, summary_file_path)
    logger.success("Type Summary Generated at: {}", summary_file_path)

    logger.info("Generating Attribute Summary")
    a_summary = generate_basic_attribute_summary(schema, v_types)
    to_yaml_file(a_summary, attribute_summary_path)
    logger.success("Attribute Summary Generated at: {}", attribute_summary_path)

    logger.info("Generating Relation Summary")
    rel_summary = generate_basic_relation_summary(schema)
    to_yaml_file(rel_summary, rel_summary_path)
    logger.success("Relation Summary Generated at: {}", rel_summary_path)


def main():
    schema, v_types = load_schema()
    generate_basics(schema, v_types)
    logger.success("All tasks completed.")


if __name__ == "__main__":
    main()
