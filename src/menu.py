"""
menu.py — Presentacion del menu en consola.

Responsabilidad unica: mostrar opciones y capturar la seleccion del usuario.
No contiene logica de negocio ni acceso a datos.
"""

_OPTIONS = [
    ("1", "Crear usuario"),
    ("2", "Listar usuarios"),
    ("3", "Actualizar usuario"),
    ("4", "Eliminar usuario"),
    ("5", "Exportar usuarios a CSV        [pandas]"),
    ("6", "Generar reporte estadistico    [pandas]"),
    ("7", "Buscar usuario por criterio    [pandas]"),
    ("8", "Salir"),
]


def show_menu() -> str:
    """
    Muestra el menu principal y devuelve la opcion elegida por el usuario.

    Returns:
        Cadena con el numero de opcion ingresado (sin validar).
    """
    print()
    for key, label in _OPTIONS:
        print(f"  {key}. {label}")
    return input("\nSeleccione opcion: ").strip()
