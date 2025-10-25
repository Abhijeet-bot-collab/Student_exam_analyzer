from typing import List
from models import Student, StudentList


def merge_sort_students(arr: List[Student]):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_students(arr[:mid])
    right = merge_sort_students(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].total() > right[j].total():  # descending
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def get_top_n(student_list: StudentList, n=3):
    arr = student_list.to_list()
    sorted_arr = merge_sort_students(arr)
    return sorted_arr[:n]


def subject_averages(student_list: StudentList):
    totals = {}
    count = 0
    cur = student_list.head
    while cur:
        for k, v in cur.marks.items():
            totals[k] = totals.get(k, 0) + v
        count += 1
        cur = cur.next
    if count == 0:
        return {}
    return {k: v / count for k, v in totals.items()}


def linear_search_by_name(student_list: StudentList, name: str):
    res = []
    cur = student_list.head
    while cur:
        if cur.name.lower() == name.lower():
            res.append(cur)
        cur = cur.next
    return res


def binary_search_by_roll(sorted_arr: List[Student], roll_no: int):
    low = 0
    high = len(sorted_arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_arr[mid].roll_no == roll_no:
            return sorted_arr[mid]
        elif sorted_arr[mid].roll_no < roll_no:
            low = mid + 1
        else:
            high = mid - 1
    return None


def sort_by_roll(student_list: StudentList):
    # returns list sorted by roll ascending
    arr = student_list.to_list()
    arr.sort(key=lambda s: s.roll_no)
    return arr
