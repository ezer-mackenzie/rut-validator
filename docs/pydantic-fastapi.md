# Pydantic y FastAPI

## Pydantic v2

Instala el extra y utiliza el import público:

```bash
pip install "rut-validator[pydantic]"
```

```python
from pydantic import BaseModel
from rut_validator.orm.pydantic import RutPydantic


class Person(BaseModel):
    name: str
    rut: RutPydantic


person = Person(name="Ana", rut="12.345.678-5")

assert isinstance(person.rut, RutPydantic)
assert person.rut == "123456785"
assert person.model_dump_json() == '{"name":"Ana","rut":"123456785"}'
```

`RutPydantic` es un subtipo estricto de `str`. Valida los tres formatos de entrada y
almacena siempre el valor normalizado.

## FastAPI

```bash
pip install "rut-validator[fastapi]"
```

```python
from fastapi import FastAPI
from pydantic import BaseModel
from rut_validator.orm.pydantic import RutPydantic

app = FastAPI()


class Person(BaseModel):
    rut: RutPydantic


@app.post("/people")
def create_person(person: Person) -> Person:
    return person
```

Una entrada inválida produce la respuesta de validación `422` habitual de
FastAPI. El JSON Schema incluye patrón, descripción y ejemplos.

## Value object enriquecido

`RutPydantic` se comporta como texto. Para acceder a `formatted`, `body` y otras
propiedades, valida el valor con el core:

```python
from rut_validator import validate_rut

rut = validate_rut(person.rut)
print(rut.formatted)
```
