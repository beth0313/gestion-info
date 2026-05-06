# gestion-info

Sistema de gestion de usuarios en consola, desarrollado en Python con buenas practicas de software.

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion de dependencias

```bash
pip install -r requirements.txt
```

| Libreria | Version minima | Uso                                               |
|----------|---------------|---------------------------------------------------|
| pandas   | 2.0.0         | Exportar CSV, reporte estadistico, filtrado dinamico |
| pytest   | 7.0.0         | Suite de pruebas automatizadas                    |

## Ejecucion

```bash
cd src
python main.py
```

## Menu de opciones

| Opcion | Descripcion                              |
|--------|------------------------------------------|
| 1      | Crear usuario                            |
| 2      | Listar usuarios                          |
| 3      | Actualizar usuario                       |
| 4      | Eliminar usuario                         |
| 5      | Exportar usuarios a CSV    `[pandas]`    |
| 6      | Generar reporte estadistico `[pandas]`   |
| 7      | Buscar usuario por criterio `[pandas]`   |
| 8      | Salir                                    |

## Ejecutar pruebas

Desde la raiz del proyecto:

```bash
pytest tests/ -v
```

Para ver solo el resumen:

```bash
pytest tests/
```

Para ver cobertura de un modulo especifico:

```bash
pytest tests/test_service.py -v
pytest tests/test_storage.py -v
pytest tests/test_integration.py -v
pytest tests/test_validate.py -v
```

La suite completa incluye **75 pruebas** que cubren:

- `test_validate.py`   — validaciones de campos (ID, nombre, email)
- `test_service.py`    — logica de negocio: crear, listar, actualizar, eliminar
- `test_storage.py`    — persistencia JSON: carga, guardado, roundtrip, errores
- `test_integration.py`— modulo pandas: DataFrame, filtros, CSV, reporte, busqueda

## Estructura del proyecto

```
gestion-info/
├── requirements.txt          # Dependencias (pandas, pytest)
├── README.md
├── src/
│   ├── main.py               # Punto de entrada y bucle principal
│   ├── menu.py               # Presentacion del menu (sin logica)
│   ├── service.py            # Logica de negocio (UserService)
│   ├── storage.py            # Persistencia JSON (load/save)
│   ├── validate.py           # Validaciones de campos
│   ├── exceptions.py         # Excepciones de dominio
│   ├── integration.py        # Modulo pandas (*args/**kwargs)
│   └── data/
│       ├── records.json           # Datos persistidos
│       └── reporte_usuarios.csv   # CSV generado por opcion 5
└── tests/
    ├── conftest.py            # Fixtures compartidos
    ├── test_validate.py       # Pruebas de validaciones
    ├── test_service.py        # Pruebas de UserService
    ├── test_storage.py        # Pruebas de storage
    └── test_integration.py    # Pruebas de integracion pandas
```

## Arquitectura y buenas practicas (Modulo 6)

### Separacion de responsabilidades

| Modulo          | Responsabilidad unica                              |
|-----------------|----------------------------------------------------|
| `main.py`       | Bucle de UI — delega todo al servicio              |
| `menu.py`       | Solo muestra opciones y captura la seleccion       |
| `service.py`    | Unico punto de mutacion de datos en memoria        |
| `storage.py`    | Solo lee/escribe JSON en disco                     |
| `validate.py`   | Todas las reglas de formato y unicidad             |
| `exceptions.py` | Jerarquia de errores de dominio                    |
| `integration.py`| Transformacion y presentacion con pandas           |

### Excepciones de dominio

Todas las excepciones heredan de `AppError`:

```
AppError
├── InvalidFieldError    — campo vacio, corto o con formato incorrecto
├── DuplicateIDError     — ID ya registrado
├── DuplicateEmailError  — email ya en uso
└── UserNotFoundError    — usuario no encontrado
```

`main.py` captura `AppError` en un solo bloque `except`, sin duplicar manejo de errores.

### Type hints y docstrings

Todos los modulos incluyen:
- Type hints en firmas de funciones y metodos
- Docstrings con descripcion, `Args:` y `Raises:` donde aplica
- Alias de tipo `UserDict = dict[str, Any]` para legibilidad
