# Línea de comandos

La instalación base expone el comando `rut-validator`.

## Validar

```bash
rut-validator validate 12.345.678-5
rut-validator validate 12.345.678-5 --json
```

La salida JSON incluye estado, formatos canónicos, cuerpo, DV y formato de
entrada. En caso de error, `--json` mantiene una salida JSON pura con `code` y
`message`, sin incluir el RUT recibido.

## Formatear

```bash
rut-validator format 123456785 --format formatted
rut-validator format 123456785 --format hyphenated
rut-validator format 123456785 --format normalized
```

También se aceptan los alias `dotted` y `numeric`.

## Información

```bash
rut-validator info 12.345.678-5
rut-validator info 12.345.678-5 --detailed
```

## Procesamiento batch

El archivo debe contener un RUT por línea:

```text
12.345.678-5
20.884.437-7
invalid
```

```bash
rut-validator batch ruts.txt
rut-validator batch ruts.txt --output result.jsonl
```

La salida usa JSON Lines. El comando termina con código `1` cuando alguna línea
es inválida y con `0` cuando todas son válidas.

## Códigos de salida

| Código | Significado |
| --- | --- |
| `0` | Operación correcta |
| `1` | Error de validación o lote parcialmente inválido |
| `2` | Uso incorrecto del comando |
