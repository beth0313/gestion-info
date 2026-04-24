from service import UserService
from file import load_data, save_data
from menu import show_menu

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

                service.create_user(user_id, name, email)
                save_data(service.list_users())

            elif option == "2":
                for u in service.list_users():
                    print(u)

            elif option == "3":
                user_id = input("ID a actualizar: ")
                name = input("Nuevo nombre: ")
                email = input("Nuevo email: ")

                service.update_user(user_id, name, email)
                save_data(service.list_users())

            elif option == "4":
                user_id = input("ID a eliminar: ")

                service.delete_user(user_id)
                save_data(service.list_users())

            elif option == "5":
                break

            else:
                print("Opción inválida")

        except ValueError as e:
            print("Error:", e)

if __name__ == "__main__":
    main()