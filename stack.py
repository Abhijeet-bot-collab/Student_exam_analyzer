class Stack:
    def __init__(self):
        self._stack = []

    def push(self, action):
        self._stack.append(action)

    def pop(self):
        return self._stack.pop() if self._stack else None

    def peek(self):
        return self._stack[-1] if self._stack else None

    def is_empty(self):
        return len(self._stack) == 0
