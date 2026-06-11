class Person:
    """Base class representing a person."""

    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name}, email={self._email})"