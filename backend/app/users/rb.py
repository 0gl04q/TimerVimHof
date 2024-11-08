from pydantic import EmailStr


class RBUser:
    def __init__(self, user_id: int | None = None, email: EmailStr | None = None, username: str | None = None):
        self.id = user_id
        self.email = email
        self.username = username

    def to_dict(self) -> dict:
        data = {'id': self.id, 'email': self.email, 'username': self.email}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
