import pytest
from models import Student, StudentList
from analysis import get_top_n, subject_averages


def make_sl():
    sl = StudentList()
    sl.append(Student(1, 'A', {'M':90,'E':80}))
    sl.append(Student(2, 'B', {'M':70,'E':60}))
    sl.append(Student(3, 'C', {'M':85,'E':75}))
    return sl


def test_top_n():
    sl = make_sl()
    top = get_top_n(sl, 2)
    assert [s.roll_no for s in top] == [1,3]


def test_subject_avg():
    sl = make_sl()
    avgs = subject_averages(sl)
    assert round(avgs['M'],2) == round((90+70+85)/3,2)
