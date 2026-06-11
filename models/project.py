from models.task import Task


class Project:
    """Represents a project belonging to a user."""

    _id_counter = 1

    def __init__(self, title: str, description: str = "", due_date: str = "", project_id: int = None):
        self.id = project_id if project_id else Project._id_counter
        if not project_id:
            Project._id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        """Add a task to this project."""
        self.tasks.append(task)

    def get_task(self, title: str):
        """Find a task by title."""
        return next((t for t in self.tasks if t.title.lower() == title.lower()), None)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        proj = cls(data["title"], data.get("description", ""), data.get("due_date", ""), data.get("id"))
        proj.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return proj

    def __str__(self):
        return f"Project({self.id}): {self.title} | Due: {self.due_date or 'N/A'} | Tasks: {len(self.tasks)}"