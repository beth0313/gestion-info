"""
main.py — Punto de entrada de la aplicacion gestion-info.

Coordina el bucle principal: muestra el menu, delega cada opcion
al servicio correspondiente y persiste los cambios.
No contiene logica de negocio ni validaciones.
"""

from exceptions import AppError
from integration import export_csv, generate_report, search_and_display
from menu import show_menu
from service import UserService
from storage import load_records, save_records


def _handle_create(service: UserService) -> None:
    user_id = input("ID: ").strip()
    name = input("Nombre: ").strip()
    email = input("Email: ").strip()
    service.create_user(user_id, name, email)
    save_records(service.list_records())
    print("  Usuario creado.")


def _handle_list(service: UserService) -> None:
    records = service.list_records()
    if not records:
        print("  No hay registros.")
        return
    for user in records:
        print(f"  [{user['id']}] {user['name']} — {user['email']}")


def _handle_update(service: UserService) -> None:
    user_id = input("ID a actualizar: ").strip()
    name = input("Nuevo nombre (Enter para omitir): ").strip()
    email = input("Nuevo email  (Enter para omitir): ").strip()
    service.update_user(user_id, name or None, email or None)
    save_records(service.list_records())
    print("  Usuario actualizado.")


def _handle_delete(service: UserService) -> None:
    user_id = input("ID a eliminar: ").strip()
    service.delete_user(user_id)
    save_records(service.list_records())
    print("  Usuario eliminado.")


def _handle_export(service: UserService) -> None:
    export_csv(service.list_records())


def _handle_report(service: UserService) -> None:
    generate_report(service.list_records())


def _handle_search(service: UserService) -> None:
    field = input("Campo a buscar (id / name / email): ").strip()
    value = input("Valor: ").strip()
    search_and_display(service.list_records(), **{field: value})


_HANDLERS = {
    "1": _handle_create,
    "2": _handle_list,
    "3": _handle_update,
    "4": _handle_delete,
    "5": _handle_export,
    "6": _handle_report,
    "7": _handle_search,
}


def main() -> None:
    """Bucle principal de la aplicacion."""
    service = UserService()
    service.load_initial_data(load_records())

    while True:
        option = show_menu()

        if option == "8":
            print("  Hasta luego.")
            break

        handler = _HANDLERS.get(option)
        if handler is None:
            print("  Opcion invalida.")
            continue

        try:
            handler(service)
        except AppError as exc:
            print(f"  Error: {exc}")
        except KeyboardInterrupt:
            print("\n  Operacion cancelada.")


if __name__ == "__main__":
    main()
