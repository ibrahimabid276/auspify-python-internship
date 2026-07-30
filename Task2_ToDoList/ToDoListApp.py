import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks):
    text = input("task description: ").strip()
    if not text:
        print("can't add an empty task")
        return

    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print("added.")


def view_tasks(tasks):
    if not tasks:
        print("no tasks yet")
        return

    print()
    for i, t in enumerate(tasks, start=1):
        status = "x" if t["done"] else " "
        print(f"{i}. [{status}] {t['text']}")
    print()


def mark_done(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    raw = input("mark which task as done? (number): ").strip()
    if not raw.isdigit():
        print("enter a valid number")
        return

    idx = int(raw) - 1
    if idx < 0 or idx >= len(tasks):
        print("no task with that number")
        return

    tasks[idx]["done"] = True
    save_tasks(tasks)
    print("marked as done.")


def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    raw = input("delete which task? (number): ").strip()
    if not raw.isdigit():
        print("enter a valid number")
        return

    idx = int(raw) - 1
    if idx < 0 or idx >= len(tasks):
        print("no task with that number")
        return

    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"deleted: {removed['text']}")


def main():
    tasks = load_tasks()

    while True:
        print("1. add task")
        print("2. view tasks")
        print("3. mark task done")
        print("4. delete task")
        print("5. quit")

        choice = input("choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("bye")
            break
        else:
            print("pick 1-5")

        print()


if __name__ == "__main__":
    main()
