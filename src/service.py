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

    def create_user(self, user_id, name, email):
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

    def list_users(self):
        return self.users

    def get_user(self, user_id):
        return next((u for u in self.users if u["id"] == user_id), None)

    def update_user(self, user_id, name=None, email=None):
        user = self.get_user(user_id)
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

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        self.users.remove(user)
        self.ids.remove(user["id"])
        self.emails.remove(user["email"])