import json
from datetime import datetime, time
from flask import Blueprint, render_template, request

to_do_bp = Blueprint('to_do', __name__, url_prefix='/to_do')

class Task:
    def __init__(self, name, due_date, duration, priority, note):
        self.name = name
        self.due_date = due_date
        self.duration = duration
        self.priority = priority
        self.note = note
        self.state = False  # Default state is set to False (not completed)

    def toggle_state(self):
        self.state = not self.state

    def to_dict(self):
        return {
            'name': self.name,
            'due_date': self.due_date.isoformat(),
            'duration': self.duration.isoformat(),
            'priority': self.priority,
            'note': self.note,
            'state': self.state
        }

    @classmethod
    def from_dict(cls, task_dict):
        name = task_dict['name']
        due_date = datetime.fromisoformat(task_dict['due_date'])
        duration = time.fromisoformat(task_dict['duration'])
        priority = task_dict['priority']
        note = task_dict['note']
        state = task_dict['state']

        task = cls(name, due_date, duration, priority, note)
        task.state = state
        return task

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_all_tasks(self):
        return self.tasks

    def save_tasks(self, file_path):
        tasks_data = [task.to_dict() for task in self.tasks]

        with open(file_path, 'w') as file:
            json.dump(tasks_data, file)

    def load_tasks(self, file_path):
        try:
            with open(file_path, 'r') as file:
                tasks_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Handle file not found or JSON decode error
            print(f"Error loading tasks: {e}")
            return

        self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]

todo_list = ToDoList()
todo_list.load_tasks('day_planning/tasks.json')

@to_do_bp.route('/', methods=['GET', 'POST'])
def to_do_home():
    if request.method == 'POST':
        # Handle task creation
        name = request.form.get('name')
        due_date = datetime.fromisoformat(request.form.get('due_date'))
        duration = time.fromisoformat(request.form.get('duration'))
        priority = int(request.form.get('priority'))
        note = request.form.get('note')

        task = Task(name, due_date, duration, priority, note)
        todo_list.add_task(task)
        todo_list.save_tasks('day_planning/tasks.json')

    tasks = todo_list.get_all_tasks()
    return render_template('day_planning/to_do.html', tasks=tasks)

@to_do_bp.route('/sort', methods=['POST'])
def sort_tasks():
    todo_list.tasks.sort(key=lambda x: x.priority)
    return render_template('day_planning/to_do.html', tasks=todo_list.tasks)

@to_do_bp.route('/load', methods=['POST'])
def load_tasks():
    todo_list.load_tasks('day_planning/tasks.json')
    return render_template('day_planning/to_do.html', tasks=todo_list.tasks)

@to_do_bp.route('/save', methods=['POST'])
def save_tasks():
    todo_list.save_tasks('day_planning/tasks.json')
    return render_template('day_planning/to_do.html', tasks=todo_list.tasks)
