import sqlite3
import json
from typing import List
from models import Student
import csv
import os

DB_FILE = 'students.db'


def init_db(path=DB_FILE):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            marks TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_all(student_list, path=DB_FILE):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('DELETE FROM students')
    for s in student_list.to_list():
        cur.execute('INSERT INTO students (roll_no, name, marks) VALUES (?, ?, ?)',
                    (s.roll_no, s.name, json.dumps(s.marks)))
    conn.commit()
    conn.close()


def load_all(path=DB_FILE):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT roll_no, name, marks FROM students ORDER BY roll_no')
    rows = cur.fetchall()
    conn.close()
    return [{'roll_no': r[0], 'name': r[1], 'marks': json.loads(r[2])} for r in rows]


# CSV helpers

def save_csv(student_list, path='students.csv'):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['roll_no', 'name', 'marks_json'])
        for s in student_list.to_list():
            writer.writerow([s.roll_no, s.name, json.dumps(s.marks)])


def load_csv(path='students.csv'):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            out.append({'roll_no': int(r['roll_no']), 'name': r['name'], 'marks': json.loads(r['marks_json'])})
    return out
