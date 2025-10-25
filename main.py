import argparse
import json
import os
import sys
from models import Student, StudentList
from stack import Stack
from analysis import get_top_n, subject_averages, sort_by_roll, linear_search_by_name
from storage import save_to_file, load_from_file
from db import init_db, save_all, load_all, save_csv, load_csv
from visualize import bar_student_marks, subject_comparison

DATA_FILE = os.path.join(os.path.dirname(__file__), 'students.json')
DB_FILE = os.path.join(os.path.dirname(__file__), 'students.db')


def print_student(s: Student):
    print(f"Roll: {s.roll_no}, Name: {s.name}, Marks: {s.marks}, Total: {s.total()}")


def load_students(student_list: StudentList, source='json'):
    if source == 'json':
        data = load_from_file(DATA_FILE)
    elif source == 'db':
        data = load_all(DB_FILE)
    elif source == 'csv':
        data = load_csv(os.path.join(os.path.dirname(__file__), 'students.csv'))
    else:
        data = []
    student_list.load_from_list(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Student Exam Result Analyzer')
    sub = parser.add_subparsers(dest='cmd')

    addp = sub.add_parser('add')
    addp.add_argument('--roll', required=True, type=int)
    addp.add_argument('--name', required=True)
    addp.add_argument('--marks', required=True, help='subject:score,subject:score')
    addp.add_argument('--save-to', choices=['json','db','csv'], default='json')

    delp = sub.add_parser('delete')
    delp.add_argument('--roll', required=True, type=int)
    delp.add_argument('--save-to', choices=['json','db','csv'], default='json')

    listp = sub.add_parser('list')
    listp.add_argument('--source', choices=['json','db','csv'], default='json')

    topp = sub.add_parser('top')
    topp.add_argument('--n', type=int, default=3)

    avgp = sub.add_parser('avg')

    searchp = sub.add_parser('search')
    searchp.add_argument('--name', required=True)

    undop = sub.add_parser('undo')

    visp = sub.add_parser('vis')
    visp.add_argument('--type', choices=['student','subject'], required=True)
    visp.add_argument('--roll', type=int)

    dbp = sub.add_parser('init-db')

    args = parser.parse_args(argv)

    sl = StudentList()
    undo_stack = Stack()

    # load from json by default to keep simple CLI state
    load_students(sl, source='json')

    if args.cmd == 'add':
        try:
            marks = {}
            for part in args.marks.split(','):
                if ':' in part:
                    k,v = part.split(':')
                    marks[k.strip()] = int(v.strip())
            student = Student(args.roll, args.name, marks)
            sl.insert_sorted_by_roll(student)
            undo_stack.push({'type':'add','student':student.to_dict()})
            print('Added')
            if args.save_to == 'json':
                save_to_file(sl, DATA_FILE)
            elif args.save_to == 'db':
                init_db(DB_FILE); save_all(sl, DB_FILE)
            else:
                save_csv(sl, os.path.join(os.path.dirname(__file__), 'students.csv'))
        except Exception as e:
            print('Error adding student:', e)
            return 1

    elif args.cmd == 'delete':
        try:
            deleted = sl.delete_by_roll(args.roll)
            if deleted:
                undo_stack.push({'type':'delete','student':deleted.to_dict()})
                print('Deleted')
            else:
                print('Not found')
            if args.save_to == 'json':
                save_to_file(sl, DATA_FILE)
            elif args.save_to == 'db':
                init_db(DB_FILE); save_all(sl, DB_FILE)
            else:
                save_csv(sl, os.path.join(os.path.dirname(__file__), 'students.csv'))
        except Exception as e:
            print('Error deleting:', e)
            return 1

    elif args.cmd == 'list':
        load_students(sl, source=args.source)
        for s in sl.to_list():
            print_student(s)

    elif args.cmd == 'top':
        top = get_top_n(sl, args.n)
        for s in top:
            print_student(s)

    elif args.cmd == 'avg':
        avgs = subject_averages(sl)
        for k,v in avgs.items():
            print(f"{k}: {v:.2f}")

    elif args.cmd == 'search':
        res = linear_search_by_name(sl, args.name)
        if not res:
            print('No matches')
        for s in res:
            print_student(s)

    elif args.cmd == 'undo':
        action = undo_stack.pop()
        if not action:
            print('Nothing to undo')
        else:
            if action['type']=='add':
                sl.delete_by_roll(action['student']['roll_no'])
                print('Undo add')
            else:
                s = action['student']
                sl.insert_sorted_by_roll(Student(s['roll_no'], s['name'], s['marks']))
                print('Undo delete')
            save_to_file(sl, DATA_FILE)

    elif args.cmd == 'vis':
        if args.type == 'subject':
            load_students(sl)
            subject_comparison(sl)
        else:
            if not args.roll:
                print('roll required for student vis')
                return 1
            load_students(sl)
            s = sl.find_by_roll(args.roll)
            if not s:
                print('not found')
                return 1
            bar_student_marks(s)

    elif args.cmd == 'init-db':
        init_db(DB_FILE)
        save_all(sl, DB_FILE)
        print('DB initialized')

    else:
        parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
