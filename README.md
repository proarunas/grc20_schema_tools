# GRC20 Schema Tools

## Overview
This repository is designed to provide the GRC20 specification in a structured format that can be easily parsed and interacted with. The GRC20 spec outlines how to store semantic knowledge graphs on the blockchain.

You can read the specification here: [GRC20 proposal](https://github.com/graphprotocol/graph-improvement-proposals/blob/main/grcs/0020-knowledge-graph.md).


## Current Capabilities
For now, this repository focuses on presenting and validating the interconnected data structures of the GRC20 specification.
Further plans include providing an easier way to define and validate custom data structures, and tools for converting data to the compatible structures.

In the meantime, the `yaml` files in the `schema` and `generated` directories can be used to get a better understanding of the GRC20 schema.


## Installation
The scripts rely on a few minor Python libraries, with `ruamel.yaml` being the most significant for YAML parsing. Details can be found in the `requirements.txt`.

## Key Files
- **generator/generator.py**: The entry point for scripts in this repository.
- **schema/base_schema.yaml**: Contains the main GRC20 schema.
- **schema/value_types.yaml**: Describes the information about the GRC20 value types (literals).
- **generated/id_dict.yaml**: Provides a quick lookup for IDs of the base entities.
- **generated/type_summary.yaml**, **attribute_summary.yaml**, **relation_summary.yaml**: Offer simplified views of the base schema for easier overview.

## Limitations
This is an early version with limited features and is based entirely on the spec. It is yet to be validated against the GRC20 implementation.

