# Guia para construir y extender rut-validator

## 1) Meta del proyecto
Construir una libreria de validacion de RUT que sea:
- reutilizable sin frameworks
- integrable con Pydantic
- utilizable en FastAPI sin acoplar el core a FastAPI
- estable para evolucionar sin romper usuarios

La regla principal es: Pydantic-first para el tipo, FastAPI como consumidor.

## 2) Arquitectura recomendada
Usa 4 capas:

1. Core
- Validacion, normalizacion, formateo y calculo del digito verificador.
- Sin dependencia de Pydantic ni FastAPI.

2. Tipos para Pydantic
- Tipo RutStr que valida usando el core.
- JSON schema para OpenAPI.
- Serializacion estable.

3. Integraciones
- Ejemplos y adaptadores opcionales para FastAPI.
- Nada de logica de negocio aqui.

4. Producto
- Tests, versionado semantico, CI, changelog y release.

## 3) Estructura base sugerida
- src/rut_validator/core/validator.py
- src/rut_validator/types/rut_str.py
- src/rut_validator/errors.py
- src/rut_validator/__init__.py
- tests/
- examples/

## 4) Contrato publico
Mantener API publica minima:
- RutValidator
- ValidatedRut
- RutStr
- RutValidationError

Todo lo demas debe considerarse interno.

## 5) Flujo de validacion
1. Entrada de usuario
2. Limpieza de espacios
3. Parseo (con o sin guion)
4. Calculo modulo 11
5. Comparacion de digito verificador
6. Normalizacion de salida
7. Formato legible opcional

Define un formato canonico y mantenlo estable. Recomendacion:
- canonico: 123456789
- visual: 12.345.678-9

## 6) Reglas para hacerlo bien
1. No mezclar parseo con render
- parseo: obtener datos estructurados
- render: representar para UI o logs

2. Errores con codigo
- invalid_format
- invalid_check_digit
- out_of_range
- empty_value

3. Mensajes claros
- para humanos: texto amigable
- para maquinas: codigo y metadata

4. Cambios compatibles
- romper comportamiento existente solo en major
- nuevas funciones en minor
- fixes en patch

## 7) Integracion correcta con Pydantic
RutStr debe:
- validar usando RutValidator
- retornar string canonico al serializar
- exponer schema JSON para docs

Recomendaciones:
- no duplicar logica de validacion dentro de RutStr
- delegar siempre al core
- tener tests que validen errores de Pydantic

## 8) Integracion con FastAPI
FastAPI no debe tener logica extra de RUT.
Usa modelos Pydantic con RutStr y deja que la validacion ocurra en el modelo.

Patron recomendado:
- request model con RutStr
- response model con string canonico y/o formato legible
- status 422 cuando el RUT no valida

## 9) Plan de implementacion por fases
Fase 1: Core
- completar casos validos e invalidos
- asegurar normalizacion
- cubrir bordes

Fase 2: Pydantic
- tipo RutStr
- schema JSON
- serializacion

Fase 3: Documentacion y ejemplos
- ejemplo puro
- ejemplo Pydantic
- ejemplo FastAPI

Fase 4: Calidad y release
- suite de tests
- CI
- versionado
- publicacion

## 10) Checklist de calidad
- tests unitarios de modulo 11
- tests parametrizados para formatos
- tests de integracion Pydantic
- tests de endpoint FastAPI
- type checking
- lint
- cobertura aceptable

## 11) Como extender sin romper
1. Agregar politicas de validacion por configuracion
- strict=True/False
- permitir o no ciertos formatos de entrada

2. Agregar nuevos tipos
- RutStrStrict
- RutStrLoose

3. Agregar utilidades
- mascara parcial para logs
- conversiones de formato

4. Mantener compatibilidad
- no cambiar salida canonica por defecto
- deprecaciones con aviso y fecha

## 12) Roadmap recomendado (4 semanas)
Semana 1
- core robusto + tests unitarios

Semana 2
- RutStr + schema + tests de integracion

Semana 3
- ejemplos + README + CI

Semana 4
- hardening + benchmark basico + release

## 13) Primer objetivo practico para este repo
1. Completar tests de core y bordes
2. Ajustar mensajes y codigos de error
3. Endurecer RutStr para serializacion y schema
4. Agregar CI minima
5. Publicar primera version estable
