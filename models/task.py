class Task:
    """Represents a task within a project."""

    _id_counter = 1

    def __init__(self, title: str, assigned_to: str = "", status: str = "pending", task_id: int = None):
        self.id = task_id if task_id else Task._id_counter
        if not task_id:
            Task._id_counter += 1
        self.title = title
        self.assigned_to = assigned_to
        self._status = status

    @property
    def status(self):
        return self._status

    def complete(self):
        """Mark task as complete."""
        self._status = "complete"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "assigned_to": self.assigned_to, "status": self._status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data.get("assigned_to", ""), data.get("status", "pending"), data.get("id"))

    def __str__(self):
        return f"[{self._status.upper()}] Task({self.id}): {self.title} → {self.assigned_to or 'unassigned'}"