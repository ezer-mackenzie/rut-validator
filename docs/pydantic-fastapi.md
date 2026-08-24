# Pydantic and FastAPI

## Pydantic v2

```bash
pip install "rut-validator[pydantic]"
```

```python
from pydantic import BaseModel

from rut_validator.integrations.pydantic import RutPydantic


class Person(BaseModel):
    name: str
    rut: RutPydantic


person = Person(name="Ana", rut="12.345.678-5")

assert isinstance(person.rut, RutPydantic)
assert person.rut == "123456785"
assert person.model_dump_json() == '{"name":"Ana","rut":"123456785"}'
```

`RutPydantic` is a strict `str` subtype. It accepts all three supported input
formats and always stores the normalized representation. Its JSON Schema
contains a description and examples. Runtime validation also checks the
modulo-11 digit, which cannot be expressed by a JSON Schema pattern.

## FastAPI

```bash
pip install "rut-validator[fastapi]"
```

```python
from fastapi import FastAPI
from pydantic import BaseModel

from rut_validator.integrations.pydantic import RutPydantic

app = FastAPI()


class Person(BaseModel):
    rut: RutPydantic


@app.post("/people")
def create_person(person: Person) -> Person:
    return person
```

Invalid input produces FastAPI's standard HTTP `422` validation response. The
same schema is included in generated OpenAPI documents.

## Access rich RUT properties

`RutPydantic` behaves as text. Use the standalone API when `formatted`, `body`,
or other rich properties are needed:

```python
from rut_validator import validate_rut

rut = validate_rut(person.rut)
print(rut.formatted)
```
