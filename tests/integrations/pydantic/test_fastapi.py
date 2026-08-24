import warnings

from fastapi import FastAPI
from starlette.exceptions import StarletteDeprecationWarning

warnings.filterwarnings(
    "ignore",
    message="Using `httpx` with `starlette.testclient` is deprecated",
    category=StarletteDeprecationWarning,
)

from fastapi.testclient import TestClient
from pydantic import BaseModel

from rut_validator.integrations.pydantic import RutPydantic


class PersonRequest(BaseModel):
    rut: RutPydantic


app = FastAPI()


@app.post("/people")
def create_person(person: PersonRequest) -> PersonRequest:
    return person


client = TestClient(app)


def test_fastapi_accepts_and_normalizes_valid_rut():
    response = client.post("/people", json={"rut": "12.345.678-5"})

    assert response.status_code == 200
    assert response.json() == {"rut": "123456785"}


def test_fastapi_rejects_invalid_rut_with_422():
    response = client.post("/people", json={"rut": "12.345.678-0"})

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error"


def test_fastapi_openapi_contains_rut_schema():
    schema = client.get("/openapi.json").json()
    rut_schema = schema["components"]["schemas"]["PersonRequest"]["properties"]["rut"]

    assert rut_schema["type"] == "string"
    assert "pattern" not in rut_schema
    assert rut_schema["examples"] == [
        "12.345.678-5",
        "12345678-5",
        "123456785",
    ]
