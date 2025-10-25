import pytest
from models import Student, StudentList


def test_student_validation():
    with pytest.raises(ValueError):
        Student(0, 'A', {'M':90})
    with pytest.raises(ValueError):
        Student(1, '', {'M':90})
    with pytest.raises(ValueError):
        Student(1, 'A', {'M':'90'})


def test_append_and_delete():
    sl = StudentList()
    s1 = Student(1, 'A', {'M':90})
    s2 = Student(2, 'B', {'M':80})
    sl.append(s1)
    sl.append(s2)
    assert len(sl) == 2
    d = sl.delete_by_roll(1)
    assert d.roll_no == 1
    assert len(sl) == 1


def test_sorted_insert():
    sl = StudentList()
    sl.insert_sorted_by_roll(Student(2, 'B', {'M':80}))
    sl.insert_sorted_by_roll(Student(1, 'A', {'M':90}))
    arr = sl.to_list()
    assert [s.roll_no for s in arr] == [1,2]
