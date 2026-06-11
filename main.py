import argparse
from models import User, Project, Task
from utils.storage import save_data, load_data
from utils.display import print_users, print_projects, print_tasks


def get_users():

    users = load_data()
    User._all = users
    return users


def cmd_add_user(args):
    users = get_users()
    if User.find(args.name):
        print(f"User '{args.name}' already exists.")
        return
    user = User(args.name, args.email or "")
    users.append(user)
    User._all = users
    save_data(users)
    print(f"✓ Added user: {user}")


def cmd_list_users(args):
    print_users(get_users())


def cmd_add_project(args):
    users = get_users()
    user = User.find(args.user)
    if not user:
        print(f"User '{args.user}' not found.")
        return
    if user.get_project(args.title):
        print(f"Project '{args.title}' already exists for {args.user}.")
        return
    proj = Project(args.title, args.description or "", args.due_date or "")
    user.add_project(proj)
    save_data(users)
    print(f"✓ Added project: {proj}")


def cmd_list_projects(args):
    users = get_users()
    user = User.find(args.user)
    if not user:
        print(f"User '{args.user}' not found.")
        return
    print_projects(user.projects, user.name)


def cmd_add_task(args):
    users = get_users()
    # Search project across all users
    for user in users:
        proj = user.get_project(args.project)
        if proj:
            if proj.get_task(args.title):
                print(f"Task '{args.title}' already exists in '{args.project}'.")
                return
            task = Task(args.title, args.assigned_to or "")
            proj.add_task(task)
            save_data(users)
            print(f"✓ Added task: {task}")
            return
    print(f"Project '{args.project}' not found.")


def cmd_list_tasks(args):
    users = get_users()
    for user in users:
        proj = user.get_project(args.project)
        if proj:
            print_tasks(proj.tasks, proj.title)
            return
    print(f"Project '{args.project}' not found.")


def cmd_complete_task(args):
    users = get_users()
    for user in users:
        proj = user.get_project(args.project)
        if proj:
            task = proj.get_task(args.title)
            if not task:
                print(f"Task '{args.title}' not found in '{args.project}'.")
                return
            task.complete()
            save_data(users)
            print(f"✓ Task marked complete: {task}")
            return
    print(f"Project '{args.project}' not found.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="project-cli",
        description="Project Management CLI Tool"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-user
    p = sub.add_parser("add-user", help="Add a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", default="")
    p.set_defaults(func=cmd_add_user)

    # list-users
    p = sub.add_parser("list-users", help="List all users")
    p.set_defaults(func=cmd_list_users)

    # add-project
    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", dest="due_date", default="")
    p.set_defaults(func=cmd_add_project)

    # list-projects
    p = sub.add_parser("list-projects", help="List projects for a user")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_list_projects)

    # add-task
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", dest="assigned_to", default="")
    p.set_defaults(func=cmd_add_task)

    # list-tasks
    p = sub.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--project", required=True)
    p.set_defaults(func=cmd_list_tasks)

    # complete-task
    p = sub.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.set_defaults(func=cmd_complete_task)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)