import json
from models import Student


def save_to_file(student_list, path):
    arr = [s.to_dict() for s in student_list.to_list()]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(arr, f, indent=2)


def load_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []
