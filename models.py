class Student:
    def __init__(self, roll_no: int, name: str, marks: dict):
        if not isinstance(roll_no, int) or roll_no <= 0:
            raise ValueError('roll_no must be a positive integer')
        if not isinstance(name, str) or not name.strip():
            raise ValueError('name must be a non-empty string')
        if not isinstance(marks, dict) or not all(isinstance(v, int) for v in marks.values()):
            raise ValueError('marks must be a dict of subject->int')

        self.roll_no = roll_no
        self.name = name.strip()
        self.marks = marks  # {'Math':85, 'CS':90, 'English':78}
        self.next = None
        self.prev = None

    def total(self):
        return sum(self.marks.values())

    def to_dict(self):
        return {'roll_no': self.roll_no, 'name': self.name, 'marks': self.marks}


class StudentList:
    """Doubly linked list of Student nodes with convenience methods.

    Supports append, delete by roll, find, convert to list and sorted insert by
    roll or by total marks.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, student: Student):
        if not isinstance(student, Student):
            raise ValueError('append expects a Student')
        if self.head is None:
            self.head = self.tail = student
            student.prev = student.next = None
        else:
            self.tail.next = student
            student.prev = self.tail
            student.next = None
            self.tail = student
        self._size += 1

    def insert_sorted_by_roll(self, student: Student):
        """Insert maintaining ascending roll_no order."""
        if not isinstance(student, Student):
            raise ValueError('insert_sorted_by_roll expects a Student')
        if self.head is None:
            self.head = self.tail = student
            student.prev = student.next = None
            self._size = 1
            return
        cur = self.head
        while cur and cur.roll_no < student.roll_no:
            cur = cur.next
        if cur is None:  # insert at end
            self.append(student)
            return
        # insert before cur
        prev = cur.prev
        student.next = cur
        student.prev = prev
        cur.prev = student
        if prev:
            prev.next = student
        else:
            self.head = student
        self._size += 1

    def insert_sorted_by_total_desc(self, student: Student):
        """Insert maintaining descending total marks order."""
        if not isinstance(student, Student):
            raise ValueError('insert_sorted_by_total_desc expects a Student')
        if self.head is None:
            self.head = self.tail = student
            student.prev = student.next = None
            self._size = 1
            return
        cur = self.head
        while cur and cur.total() >= student.total():
            cur = cur.next
        if cur is None:
            self.append(student)
            return
        prev = cur.prev
        student.next = cur
        student.prev = prev
        cur.prev = student
        if prev:
            prev.next = student
        else:
            self.head = student
        self._size += 1

    def delete_by_roll(self, roll_no: int):
        prev = None
        cur = self.head
        while cur:
            if cur.roll_no == roll_no:
                # unlink cur
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                cur.next = cur.prev = None
                self._size -= 1
                return cur
            cur = cur.next
        return None

    def find_by_roll(self, roll_no: int):
        cur = self.head
        while cur:
            if cur.roll_no == roll_no:
                return cur
            cur = cur.next
        return None

    def find_by_name(self, name: str):
        cur = self.head
        res = []
        while cur:
            if cur.name.lower() == name.lower():
                res.append(cur)
            cur = cur.next
        return res

    def to_list(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur)
            cur = cur.next
        return arr

    def clear(self):
        self.head = self.tail = None
        self._size = 0

    def load_from_list(self, students, insert_sorted=False, by_total=False):
        """Load from list of dicts. If insert_sorted=True will insert in sorted order.

        by_total toggles sorting key for sorted insert (total desc) otherwise by roll.
        """
        self.clear()
        for s in students:
            st = Student(s['roll_no'], s['name'], s['marks'])
            if insert_sorted:
                if by_total:
                    self.insert_sorted_by_total_desc(st)
                else:
                    self.insert_sorted_by_roll(st)
            else:
                self.append(st)
