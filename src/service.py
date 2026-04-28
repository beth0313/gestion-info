from validate import validate_id, validate_name, validate_email

class UserService:
    def __init__(self):
        self.users = []
        self.ids = set()
        self.emails = set()

    def load_initial_data(self, data):
        self.users = data
        self.ids = {u["id"] for u in data}
        self.emails = {u["email"] for u in data}

    def new_register(self, user_id, name, email):
        validate_id(user_id, self.ids)
        validate_name(name)
        validate_email(email, self.emails)

        user = {
            "id": user_id,
            "name": name,
            "email": email
        }

        self.users.append(user)
        self.ids.add(user_id)
        self.emails.add(email)

    def list_records(self):
        # Uso de lambda para ordenar por ID
        return sorted(self.users, key=lambda x: x["id"])

    def search_record(self, user_id):
        # Uso de list comprehension para buscar
        matching = [u for u in self.users if u["id"] == user_id]
        return matching[0] if matching else None

    def update_record(self, user_id, name=None, email=None):
        user = self.search_record(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        if name:
            validate_name(name)
            user["name"] = name

        if email:
            if email != user["email"]:
                validate_email(email, self.emails)
                self.emails.remove(user["email"])
                self.emails.add(email)
                user["email"] = email

    def delete_record(self, user_id):
        user = self.search_record(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        self.users.remove(user)
        self.ids.remove(user["id"])
        self.emails.remove(user["email"])