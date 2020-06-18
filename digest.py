import base64
import hashlib
import json
from pathlib import Path

import brotli
import pytest
import yaml


def sha256_algorithm(*a, **k):
    return base64.encodebytes(hashlib.sha256(*a, **k).digest())


def sha512_algorithm(*a, **k):
    return base64.encodebytes(hashlib.sha512(*a, **k).digest())

DIGEST_ALGORITHMS = {
    'sha256': sha256_algorithm,
    'id-sha-512': sha512_algorithm,
    'identity': lambda x: x,
    'br': brotli.compress
}


def digest(_bytes, algorithm=sha256_algorithm, parameters=None):
    parameters = parameters or {}
    checksum_bytes = algorithm(_bytes, **parameters)
    return checksum_bytes.strip()


def digest_json(item, content_coding=lambda x: x, algorithm=hashlib.sha256):
    json_bytes = json.dumps(item).encode()
    encoded_bytes = content_coding(json_bytes)
    return digest(encoded_bytes, algorithm)


def parse(field_value):
    for representation_digest in field_value.split(","):
        algorithm, value = representation_digest.strip().split("=", 1)
        value, *params = value.split(";", 1)
        parameters = (
            dict(x.split("=", 1) for x in params[0].split(";")) if params else {}
        )
        yield {
            "algorithm": algorithm.lower(),
            "parameters": parameters,
            "value": value,
        }


#
# Tests
#
def testlist():
    return yaml.safe_load(Path("testlist.yaml").read_text())


@pytest.mark.parametrize("_input", testlist()["test-parse-ok"])
def test_ok(_input):
    name, field_value, expected = _input.values()
    for d in parse(field_value):
        assert d in expected

@pytest.mark.parametrize("_input", testlist()["test-checksum-ok"])
def test_ok(_input):
    name, algorithm, _bytes, content_coding, expected = _input.values()
    _bytes = _bytes.encode()
    digest_algorithm = algorithm['algorithm']
    algorithm_f = DIGEST_ALGORITHMS[digest_algorithm]
    if content_coding and not digest_algorithm.startswith('id-'):
        _bytes = DIGEST_ALGORITHMS[content_coding](_bytes)
    parameters = algorithm.get('parameters')
    d = digest(_bytes, algorithm_f, parameters=parameters)
    assert d.decode() == expected


