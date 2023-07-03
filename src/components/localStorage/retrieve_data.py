import webview
import json


def retrieve_data():
    # Retrieve the stored tasks from local storage
    stored_tasks = webview.evaluate_js('localStorage.getItem("tasks")')

    # Parse the JSON data into a Python object
    task_data = json.loads(stored_tasks)

    # Print the task data
    print(task_data)


if __name__ == '__main__':
    webview.create_window(
        "Retrieve Data", html='<html><body><script src="localStorageUtils.js"></script><script>retrieve_data()</script></body></html>')
    webview.start()
