# -*- coding: utf-8 -*-
"""
"""
import json
from io import StringIO
from pathlib import Path

import pytest
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError


METASCHEMA_FILE = Path("metaschema.json")
# JsonSchema 2.6.0 only supports draft-04 at the time of this writing
METASCHEMA_URL = "http://json-schema.org/draft-04/schema"
SCHEMAS = list(f for f in Path('./schemas').iterdir() if f.suffix == ".json")


@pytest.fixture
def metaschema():
    resp = requests.get(METASCHEMA_URL, stream=True)
    stream = StringIO(resp.content.decode('utf-8'))
    data = json.load(stream)
    return data


@pytest.mark.parametrize("schema", SCHEMAS)
def test_valid_json(schema):
    with open(str(schema), 'r') as openf:
        try:
            json.load(openf)
        except Exception:
            pytest.fail("Invalid JSON file.")


@pytest.mark.parametrize("schema", SCHEMAS)
def test_valid_jsonschema(metaschema, schema):
    with open(str(schema), 'r') as openf:
        data = json.load(openf)
        try:
            validate(data, metaschema)
        except ValidationError as err:
            msg = "Invalid JsonSchema file `{}`. Message:\n{}"
            pytest.fail(msg.format(schema, str(err)))
        except Exception as err:
            msg = ("Unknown exception when validating JsonSchema file {}\n"
                   "  Message: {}")
            pytest.fail(msg.format(schema, str(err)))


@pytest.mark.parametrize("schema", SCHEMAS)
def test_sample_file(schema):
    # Make sure we have a sample file.
    name = Path(".".join(schema.name.split(".")[3:]))
    sample_file = schema.parent.parent / Path("samples") / name
    if not sample_file.exists():
        msg = "Sample file {} not found."
        pytest.fail(msg.format(str(sample_file)))

    with open(str(schema), 'r') as schema_file:
        schema_data = json.load(schema_file)
        with open(str(sample_file), 'r') as openf:
            data = json.load(openf)
            try:
                validate(data, schema_data)
            except ValidationError as err:
                msg = ("Sample file validation failed.\n"
                       "  Schema: {}\n"
                       "  Sample: {}")
                pytest.fail(msg.format(schema, sample_file))
            except Exception as err:
                msg = ("Unknown exception occured when validating."
                       "  Schema: {}\n"
                       "  Sample: {}\n"
                       "  Message: {}")
                pytest.fail(msg.format(schema, sample_file, str(err)))
