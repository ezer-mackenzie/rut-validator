# Versionado y releases

El proyecto sigue Semantic Versioning.

- `0.x`: la API continúa estabilizándose.
- `1.x`: contrato público estable.
- Los tipos bajo `rut_validator.core`, la lógica bajo
  `rut_validator.validation` y los adapters bajo `rut_validator.orm` forman la
  arquitectura pública.

## Gate de release

Una versión sólo debe etiquetarse cuando:

1. tests, lint y tipos pasan;
2. MkDocs construye en modo estricto;
3. wheel y sdist se construyen;
4. `twine check` valida ambos artefactos;
5. el wheel base importa en un entorno sin extras;
6. changelog y versión coinciden.

La validación de RUT no certifica identidad ni existencia ante el SII.
