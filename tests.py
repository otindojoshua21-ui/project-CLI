"""tests.py — Unit tests for models and CLI logic."""
import sys
import os
import json
import unittest
import tempfile

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from models import User, Project, Task
from models.person import Person


class TestPerson(unittest.TestCase):
    def test_init(self):
        p = Person("Alice", "alice@test.com")
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.email, "alice@test.com")

    def test_name_setter(self):
        p = Person("Bob", "")
        p.name = "Robert"
        self.assertEqual(p.name, "Robert")

    def test_empty_name_raises(self):
        p = Person("Sam", "")
        with self.assertRaises(ValueError):
            p.name = ""


class TestTask(unittest.TestCase):
    def test_create(self):
        t = Task("Write tests", "Dev")
        self.assertEqual(t.title, "Write tests")
        self.assertEqual(t.assigned_to, "Dev")
        self.assertEqual(t.status, "pending")

    def test_complete(self):
        t = Task("Deploy")
        t.complete()
        self.assertEqual(t.status, "complete")

    def test_to_dict(self):
        t = Task("Review PR", "Alice", "pending", 99)
        d = t.to_dict()
        self.assertEqual(d["title"], "Review PR")
        self.assertEqual(d["id"], 99)

    def test_from_dict(self):
        d = {"id": 5, "title": "Fix bug", "assigned_to": "Bob", "status": "complete"}
        t = Task.from_dict(d)
        self.assertEqual(t.status, "complete")
        self.assertEqual(t.title, "Fix bug")

    def test_str(self):
        t = Task("Test", task_id=1)
        self.assertIn("PENDING", str(t))


class TestProject(unittest.TestCase):
    def test_create(self):
        p = Project("My App", "Cool app", "2025-12-01", project_id=10)
        self.assertEqual(p.title, "My App")
        self.assertEqual(len(p.tasks), 0)

    def test_add_task(self):
        p = Project("Backend", project_id=20)
        t = Task("Setup DB", task_id=1)
        p.add_task(t)
        self.assertEqual(len(p.tasks), 1)

    def test_get_task(self):
        p = Project("Frontend", project_id=21)
        t = Task("Build UI", task_id=2)
        p.add_task(t)
        found = p.get_task("build ui")
        self.assertIsNotNone(found)

    def test_get_task_missing(self):
        p = Project("Empty", project_id=22)
        self.assertIsNone(p.get_task("nothing"))

    def test_to_dict_from_dict(self):
        p = Project("Roundtrip", project_id=30)
        p.add_task(Task("T1", task_id=100))
        d = p.to_dict()
        p2 = Project.from_dict(d)
        self.assertEqual(p2.title, "Roundtrip")
        self.assertEqual(len(p2.tasks), 1)


class TestUser(unittest.TestCase):
    def setUp(self):
        User._all = []

    def test_create(self):
        u = User("Charlie", "c@test.com", user_id=1)
        self.assertEqual(u.name, "Charlie")
        self.assertEqual(u.email, "c@test.com")

    def test_add_project(self):
        u = User("Dana", user_id=2)
        p = Project("P1", project_id=1)
        u.add_project(p)
        self.assertEqual(len(u.projects), 1)

    def test_get_project(self):
        u = User("Eve", user_id=3)
        p = Project("Alpha", project_id=2)
        u.add_project(p)
        self.assertIsNotNone(u.get_project("alpha"))
        self.assertIsNone(u.get_project("beta"))

    def test_find(self):
        u = User("Frank", user_id=4)
        User._all = [u]
        self.assertEqual(User.find("frank"), u)
        self.assertIsNone(User.find("ghost"))

    def test_to_dict_from_dict(self):
        u = User("Grace", "g@test.com", user_id=5)
        p = Project("Proj", project_id=3)
        p.add_task(Task("T", task_id=50))
        u.add_project(p)
        d = u.to_dict()
        u2 = User.from_dict(d)
        self.assertEqual(u2.name, "Grace")
        self.assertEqual(len(u2.projects), 1)
        self.assertEqual(len(u2.projects[0].tasks), 1)


class TestStorage(unittest.TestCase):
    def test_save_and_load(self):
        import utils.storage as storage
        with tempfile.TemporaryDirectory() as tmpdir:
            storage.DATA_FILE = os.path.join(tmpdir, "data.json")
            u = User("Henry", "h@test.com", user_id=99)
            p = Project("StorageProj", project_id=99)
            p.add_task(Task("StorageTask", task_id=99))
            u.add_project(p)
            storage.save_data([u])
            loaded = storage.load_data()
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0].name, "Henry")
            self.assertEqual(len(loaded[0].projects), 1)

    def test_load_missing_file(self):
        import utils.storage as storage
        with tempfile.TemporaryDirectory() as tmpdir:
            storage.DATA_FILE = os.path.join(tmpdir, "missing.json")
            result = storage.load_data()
            self.assertEqual(result, [])


class TestCLICommands(unittest.TestCase):
    """Integration tests for CLI command functions."""

    def setUp(self):
        import utils.storage as storage
        self._tmpdir = tempfile.mkdtemp()
        storage.DATA_FILE = os.path.join(self._tmpdir, "test_data.json")
        User._all = []
        # Reset ID counters
        User._id_counter = 1

    def _args(self, **kwargs):
        """Build a simple namespace."""
        return type("Args", (), kwargs)()

    def test_add_and_list_user(self):
        import main
        main.cmd_add_user(self._args(name="Ivy", email="ivy@test.com"))
        users = main.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Ivy")

    def test_duplicate_user(self, capsys=None):
        import main
        main.cmd_add_user(self._args(name="Jack", email=""))
        main.cmd_add_user(self._args(name="Jack", email=""))
        users = main.get_users()
        self.assertEqual(len(users), 1)

    def test_add_project(self):
        import main
        main.cmd_add_user(self._args(name="Kim", email=""))
        main.cmd_add_project(self._args(user="Kim", title="KimProj", description="", due_date=""))
        users = main.get_users()
        self.assertEqual(len(users[0].projects), 1)

    def test_add_task(self):
        import main
        main.cmd_add_user(self._args(name="Leo", email=""))
        main.cmd_add_project(self._args(user="Leo", title="LeoProj", description="", due_date=""))
        main.cmd_add_task(self._args(project="LeoProj", title="LeoTask", assigned_to=""))
        users = main.get_users()
        self.assertEqual(len(users[0].projects[0].tasks), 1)

    def test_complete_task(self):
        import main
        main.cmd_add_user(self._args(name="Mia", email=""))
        main.cmd_add_project(self._args(user="Mia", title="MiaProj", description="", due_date=""))
        main.cmd_add_task(self._args(project="MiaProj", title="MiaTask", assigned_to=""))
        main.cmd_complete_task(self._args(project="MiaProj", title="MiaTask"))
        users = main.get_users()
        self.assertEqual(users[0].projects[0].tasks[0].status, "complete")

    def test_project_not_found(self):
        import main
        # Should not crash, just print message
        main.cmd_add_task(self._args(project="Ghost", title="T", assigned_to=""))

    def test_user_not_found_for_project(self):
        import main
        main.cmd_add_project(self._args(user="Nobody", title="X", description="", due_date=""))


if __name__ == "__main__":
    unittest.main(verbosity=2)