import os
import json
from models import Student, StudentList
from db import save_csv, load_csv, init_db, save_all, load_all


def make_sl():
    sl = StudentList()
    sl.append(Student(10, 'X', {'M':90}))
    sl.append(Student(11, 'Y', {'M':80}))
    return sl


def test_csv_roundtrip(tmp_path):
    sl = make_sl()
    path = tmp_path / 'test.csv'
    save_csv(sl, path=str(path))
    loaded = load_csv(path=str(path))
    assert len(loaded) == 2
    assert loaded[0]['roll_no'] == 10


def test_db_roundtrip(tmp_path):
    dbpath = tmp_path / 'test.db'
    init_db(path=str(dbpath))
    sl = make_sl()
    save_all(sl, path=str(dbpath))
    loaded = load_all(path=str(dbpath))
    assert len(loaded) == 2
    assert loaded[1]['roll_no'] == 11
