from models.person import Person
from models.project import Project


class User(Person):
    """Represents a system user who owns projects."""

    _id_counter = 1
    _all: list["User"] = []

    def __init__(self, name: str, email: str = "", user_id: int = None):
        super().__init__(name, email)
        self.id = user_id if user_id else User._id_counter
        if not user_id:
            User._id_counter += 1
        self.projects: list[Project] = []

    def add_project(self, project: Project):
        """Attach a project to this user."""
        self.projects.append(project)

    def get_project(self, title: str):
        """Find a project by title."""
        return next((p for p in self.projects if p.title.lower() == title.lower()), None)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"], data.get("email", ""), data.get("id"))
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return user

    @classmethod
    def find(cls, name: str):
        """Find a user by name from the in-memory list."""
        return next((u for u in cls._all if u.name.lower() == name.lower()), None)

    def __str__(self):
        return f"User({self.id}): {self.name} <{self.email}> | Projects: {len(self.projects)}"