from service import UserService
from file import load_data, save_data
from menu import show_menu
from integration import export_csv, generate_report, search_and_display

def main():
    service = UserService()
    data = load_data()
    service.load_initial_data(data)

    while True:
        option = show_menu()

        try:
            if option == "1":
                user_id = input("ID: ")
                name = input("Nombre: ")
                email = input("Email: ")

                service.new_register(user_id, name, email)
                save_data(service.list_records())

            elif option == "2":
                records = service.list_records()
                if not records:
                    print("  No hay registros.")
                for u in records:
                    print(u)

            elif option == "3":
                user_id = input("ID a actualizar: ")
                name = input("Nuevo nombre: ")
                email = input("Nuevo email: ")

                service.update_record(user_id, name, email)
                save_data(service.list_records())

            elif option == "4":
                user_id = input("ID a eliminar: ")

                service.delete_record(user_id)
                save_data(service.list_records())

            # --- Opciones Modulo 5 (pandas) ---

            elif option == "5":
                export_csv(service.list_records())

            elif option == "6":
                generate_report(service.list_records())

            elif option == "7":
                campo = input("Campo a buscar (id / name / email): ").strip()
                valor = input("Valor: ").strip()
                search_and_display(service.list_records(), **{campo: valor})

            elif option == "8":
                break

            else:
                print("Opcion invalida")

        except ValueError as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
