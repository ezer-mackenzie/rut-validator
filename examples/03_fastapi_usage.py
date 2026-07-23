"""
Example 3: Using RutPydantic with FastAPI

This shows how RutPydantic automatically validates RUTs
in FastAPI request/response models.

Run with:
    pip install fastapi uvicorn
    uvicorn 03_fastapi_usage:app --reload

Then visit:
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel
from rut_validator import RutValidator
from rut_validator.orm.pydantic import RutPydantic

app = FastAPI(title="RUT Validator API")


class Person(BaseModel):
    name: str
    rut: RutPydantic  # ✅ Automatically validated by Pydantic


class PersonResponse(BaseModel):
    name: str
    rut: str
    rut_formatted: str
    rut_number: int
    rut_digit: str


@app.get("/")
def root():
    return {
        "message": "RUT Validator API",
        "endpoints": [
            "POST /person",
            "POST /persons",
            "GET /docs (OpenAPI/Swagger documentation)",
        ],
    }


@app.post("/person", response_model=PersonResponse)
def create_person(person: Person) -> PersonResponse:
    """
    Create a person with validated RUT.

    **Request:**
    ```json
    {
        "name": "Juan Pérez",
        "rut": "12345678-5"
    }
    ```

    **Response:**
    ```json
    {
        "name": "Juan Pérez",
        "rut": "123456785",
        "rut_formatted": "12.345.678-9",
        "rut_number": 12345678,
        "rut_digit": "5"
    }
    ```

    Returns 422 Unprocessable Entity if RUT is invalid.
    """
    value = RutValidator.validate(person.rut)
    return PersonResponse(
        name=person.name,
        rut=str(person.rut),
        rut_formatted=value.formatted,
        rut_number=value.body,
        rut_digit=value.check_digit,
    )


@app.post("/persons")
def create_persons(persons: list[Person]) -> dict:
    """
    Create multiple people with validated RUTs.

    **Request:**
    ```json
    [
        {
            "name": "Juan Pérez",
            "rut": "12345678-5"
        },
        {
            "name": "María García",
            "rut": "98765432-1"
        }
    ]
    ```
    """
    return {
        "count": len(persons),
        "persons": [
            {
                "name": p.name,
                "rut": RutValidator.validate(p.rut).formatted,
            }
            for p in persons
        ],
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("RUT Validator API - FastAPI Example")
    print("=" * 60)
    print("\n🚀 Starting server on http://localhost:8000")
    print("\n📖 Documentation: http://localhost:8000/docs")
    print("\n✅ Try these JSON requests in /docs:")
    print("""
   POST /person
   {
       "name": "Juan Pérez",
       "rut": "12345678-5"
   }

   POST /person (invalid RUT - returns 422)
   {
       "name": "Juan Pérez",
       "rut": "12345678-1"
   }
    """)
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
