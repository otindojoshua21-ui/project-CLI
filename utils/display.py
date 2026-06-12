
try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    RICH = True
except ImportError:
    RICH = False

def print_users(users):
    """Print all users in a table."""
    if not users:
        _out("No users found.")
        return
    if RICH:
        t = Table(title="Users")
        for col in ("ID", "Name", "Email", "Projects"):
            t.add_column(col)
        for u in users:
            t.add_row(str(u.id), u.name, u.email, str(len(u.projects)))
        console.print(t)
    else:
        for u in users:
            print(u)

def print_projects(projects, user_name=""):
    """Print projects in a table."""
    if not projects:
        _out(f"No projects found{' for ' + user_name if user_name else ''}.")
        return
    if RICH:
        t = Table(title=f"Projects{' — ' + user_name if user_name else ''}")
        for col in ("ID", "Title", "Description", "Due Date", "Tasks"):
            t.add_column(col)
        for p in projects:
            t.add_row(str(p.id), p.title, p.description, p.due_date or "N/A", str(len(p.tasks)))
        console.print(t)
    else:
        for p in projects:
            print(p)

def print_tasks(tasks, project_name=""):
    """Print tasks in a table."""
    if not tasks:
        _out(f"No tasks found{' in ' + project_name if project_name else ''}.")
        return
    if RICH:
        t = Table(title=f"Tasks{' — ' + project_name if project_name else ''}")
        for col in ("ID", "Title", "Assigned To", "Status"):
            t.add_column(col)
        for task in tasks:
            t.add_row(str(task.id), task.title, task.assigned_to or "—", task.status)
        console.print(t)
    else:
        for task in tasks:
            print(task)

def _out(msg):
    if RICH:
        console.print(msg)
    else:
        print(msg)