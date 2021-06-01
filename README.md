[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

# Agresso query engine client

Python client for Agresso query engine service.

## Usage

```python
from agresso_query_engine_client import AgressoQueryEngineClient

client = AgressoQueryEngineClient(
    username="username",
    password="password",
    client="FOO",
    service_url="https://foo.bar/baz/service.svc"
)

template_id = 42
data = client.get_template_result_as_xml(template_id)
```

## Installation

Pip: `pip install git+https://github.com/milinnovations/agresso-query-engine-client.git#egg=agresso-query-engine-client`

Pipenv: `pipenv install git+https://github.com/milinnovations/agresso-query-engine-client.git#egg=agresso-query-engine-client`

## License - MIT

The library is open-sourced under the conditions of the MIT [license](https://choosealicense.com/licenses/mit/).
