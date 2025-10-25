import tkinter as tk
from tkinter import simpledialog, messagebox
from models import Student, StudentList
from storage import save_to_file, load_from_file
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'students.json')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Exam Analyzer')
        self.geometry('600x400')
        self.sl = StudentList()
        self.load()

        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(fill='both', expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text='Add', command=self.add).pack(side='left')
        tk.Button(btn_frame, text='Delete', command=self.delete).pack(side='left')
        tk.Button(btn_frame, text='Refresh', command=self.refresh).pack(side='left')
        tk.Button(btn_frame, text='Save', command=self.save).pack(side='right')

        self.refresh()

    def load(self):
        data = load_from_file(DATA_FILE)
        self.sl.load_from_list(data)

    def refresh(self):
        self.listbox.delete(0, 'end')
        for s in self.sl.to_list():
            self.listbox.insert('end', f"{s.roll_no} - {s.name} - {s.marks} - Total:{s.total()}")

    def add(self):
        try:
            roll = int(simpledialog.askstring('Roll', 'Roll no:'))
            name = simpledialog.askstring('Name', 'Name:')
            marks_raw = simpledialog.askstring('Marks', 'subject:score,subject:score')
            marks = {}
            for p in marks_raw.split(','):
                k,v = p.split(':')
                marks[k.strip()] = int(v.strip())
            s = Student(roll, name, marks)
            self.sl.insert_sorted_by_roll(s)
            self.refresh()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def delete(self):
        try:
            sel = self.listbox.curselection()
            if not sel:
                return
            text = self.listbox.get(sel[0])
            roll = int(text.split('-')[0].strip())
            self.sl.delete_by_roll(roll)
            self.refresh()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def save(self):
        save_to_file(self.sl, DATA_FILE)
        messagebox.showinfo('Saved', 'Saved to JSON')


if __name__ == '__main__':
    App().mainloop()
