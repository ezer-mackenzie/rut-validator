# Versionado y releases

El proyecto sigue Semantic Versioning.

- `0.x`: la API continúa estabilizándose.
- `1.x`: contrato público estable.
- Los tipos bajo `rut_validator.core`, la lógica bajo
  `rut_validator.validation` y los adapters bajo `rut_validator.orm` forman la
  arquitectura pública.

## Compatibilidad de 1.x

- Python 3.10 a 3.14 se valida en CI.
- La instalación base sólo depende de Click y no importa frameworks
  opcionales.
- Pydantic 2.x, SQLAlchemy 2.x, Django 4.2–5.x, SQLModel 0.x y FastAPI 0.x se
  prueban mediante extras independientes.
- Los nombres documentados en la referencia de API son públicos. Los detalles
  con prefijo `_` siguen siendo internos.

## Deprecaciones

Un símbolo público no se eliminará en una versión menor. Primero emitirá
`DeprecationWarning`, se documentará en el changelog y se mantendrá durante al
menos una versión menor. Su eliminación sólo podrá ocurrir en una nueva versión
mayor.

## Gate de release

Una versión sólo debe etiquetarse cuando:

1. tests, lint y tipos pasan;
2. MkDocs construye en modo estricto;
3. wheel y sdist se construyen;
4. `twine check` valida ambos artefactos;
5. el wheel base importa en un entorno sin extras;
6. las dependencias no tienen vulnerabilidades conocidas;
7. changelog y versión coinciden.

La validación de RUT no certifica identidad ni existencia ante el SII.
