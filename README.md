
[![License](https://img.shields.io/github/license/ioggstream/digest-headers.svg)](https://github.com/ioggstream/digest-headers/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/ioggstream/digest-headers.svg)](https://github.com/ioggstream/digest-headers/issues)

# Digest Headers parser

> A python implementation of digest fields defined in [Digest Fields](https://github.com/httpwg/http-extensions/blob/master/draft-ietf-httpbis-digest-headers.md)


# Index

- [Quickstart](#quickstart)
- [Contribute](#contribute)
- [Licenza](#licenza)

# Quickstart

```python

import digest
import json

expected_field_value = "id-sha-256=..., sha-512=..."
representation_data = b'{"hello": "world"}'

field_value = digest.create(representation_data, digest_algorithm="sha-256")
assert field_value == 


```

# Contribute

Join the discussion on the HTTP Workgroup mailing list or 
the https://github.com/httpwg/http-extensions github repo.

### Issues

Issues can be opened on [![GitHub issues](https://img.shields.io/github/issues/ioggstream/digest-headers.svg)](https://github.com/ioggstream/digest-headers/issues)


# License 

BSD-3-Clause
