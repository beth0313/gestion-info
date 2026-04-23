from validate import validate_id, validate_name, validate_email

class UserService:
    def __init__(self):
        self.users = []
        self.ids = set()
        self.emails = set()

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