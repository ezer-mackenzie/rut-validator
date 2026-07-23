# Versionado y releases

El proyecto sigue Semantic Versioning.

- `0.x`: la API continúa estabilizándose.
- `1.x`: contrato público estable.
- Los adapters bajo `rut_validator.orm` y `rut_validator.core.orm` son rutas de
  compatibilidad; los imports cortos documentados son la API recomendada.

## Gate de release

Una versión sólo debe etiquetarse cuando:

1. tests, lint y tipos pasan;
2. MkDocs construye en modo estricto;
3. wheel y sdist se construyen;
4. `twine check` valida ambos artefactos;
5. el wheel base importa en un entorno sin extras;
6. changelog y versión coinciden.

La validación de RUT no certifica identidad ni existencia ante el SII.
