from service import UserService

def main():
    service = UserService()

    try:
        service.create_user("1", "Elizabeth", "eli@mail.com")
        service.create_user("2", "Juan", "juan@mail.com")

        # Prueba de duplicado
        service.create_user("1", "Pedro", "pedro@mail.com")

    except ValueError as e:
        print("Error:", e)

    print("\nLista de usuarios:")
    for user in service.list_users():
        print(user)


if __name__ == "__main__":
    main()