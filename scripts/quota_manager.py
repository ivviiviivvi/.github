import json
from datetime import datetime

SUBSCRIPTIONS_FILE = ".github/subscriptions.json"

def get_subscriptions():
    """Reads the subscriptions file and returns the subscriptions data."""
    try:
        with open(SUBSCRIPTIONS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"subscriptions": []}

def save_subscriptions(data):
    """Saves the subscriptions data to the subscriptions file."""
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_usage(subscription_name):
    """Gets the current usage for a specific subscription."""
    data = get_subscriptions()
    for sub in data["subscriptions"]:
        if sub["name"] == subscription_name:
            return sub.get("usage", 0)
    return 0

def increment_usage(subscription_name, amount=1):
    """Increments the usage for a specific subscription."""
    data = get_subscriptions()
    for sub in data["subscriptions"]:
        if sub["name"] == subscription_name:
            sub["usage"] = sub.get("usage", 0) + amount
            break
    save_subscriptions(data)

def reset_quotas():
    """Resets the usage for subscriptions based on their reset cadence."""
    data = get_subscriptions()
    today = datetime.now()
    for sub in data["subscriptions"]:
        last_reset = datetime.strptime(sub["last_reset"], "%Y-%m-%d")
        if sub["reset_cadence"] == "daily":
            if last_reset.date() != today.date():
                sub["usage"] = 0
                sub["last_reset"] = today.strftime("%Y-%m-%d")
        elif sub["reset_cadence"] == "monthly":
            if today.month != last_reset.month or today.year != last_reset.year:
                sub["usage"] = 0
                sub["last_reset"] = today.strftime("%Y-%m-%d")
    save_subscriptions(data)

TASK_QUEUE_FILE = ".github/task_queue.json"

def add_task_to_queue(task):
    """Adds a task to the task queue."""
    try:
        with open(TASK_QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        queue = []
    queue.append(task)
    with open(TASK_QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

def get_tasks_from_queue():
    """Retrieves all tasks from the task queue."""
    try:
        with open(TASK_QUEUE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def remove_task_from_queue(task):
    """Removes a specific task from the task queue."""
    queue = get_tasks_from_queue()
    new_queue = [t for t in queue if t != task]
    with open(TASK_QUEUE_FILE, "w") as f:
        json.dump(new_queue, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get_usage":
            print(get_usage(sys.argv[2]))
        elif command == "increment_usage":
            increment_usage(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1)
        elif command == "reset_quotas":
            reset_quotas()
        elif command == "add_task":
            add_task_to_queue(json.loads(sys.argv[2]))
        elif command == "get_tasks":
            print(json.dumps(get_tasks_from_queue()))
        elif command == "remove_task":
            remove_task_from_queue(json.loads(sys.argv[2]))
