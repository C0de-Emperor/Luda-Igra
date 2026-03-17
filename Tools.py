class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self, *elements):
        self.front = None
        self.rear = None

        for element in elements:
            self.enqueue(element)

    def __repr__(self):
        values = []
        current = self.front

        while current:
            values.append(str(current.value))
            current = current.next

        return "Queue(" + ", ".join(values) + ")"

    def enqueue(self, value):
        new_node = Node(value)

        if self.rear is None:
            self.front = self.rear = new_node
            return

        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")

        value = self.front.value
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return value

    def isEmpty(self):
        return self.front is None
    
    def rotate(self):
        if not self.isEmpty():
            self.enqueue(self.dequeue())

    def peek(self):
        if self.front:
            return self.front.value
        return None