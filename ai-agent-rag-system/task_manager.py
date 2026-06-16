class TaskManager:

    def __init__(self):
        self.tasks = []
        self.completed = []

    def add_task(self, task):
        self.tasks.append(task)

    def next_task(self):

        if not self.tasks:
            return None

        return self.tasks.pop(0)

    def complete_task(self, task):
        self.completed.append(task)

    def has_tasks(self):
        return len(self.tasks) > 0