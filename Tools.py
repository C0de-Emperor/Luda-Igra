from typing import Generic, TypeVar

T = TypeVar("T")

class Queue(Generic[T]):
    def __init__(self, *elements: T):
        self.elements=list(elements)

    def __repr__(self):
        return "Queue(" + ", ".join(self.elements) + ")"

    def enqueue(self, value: T):
        self.elements.append(value)

    def dequeue(self) -> T:
        if self.isEmpty():
            raise IndexError("Queue is empty")

        return self.elements.pop(0)
    
    def getLen(self) -> int:
        return len(self.elements)

    def isEmpty(self) -> bool:
        return len(self.elements) == 0
    
    def rotate(self):
        elements=[self.dequeue() for k in range(self.getLen())]

        for k in range(len(elements)-1, 0, -1):
            self.enqueue(elements[k])

    def peek(self):
        if not self.isEmpty():
            return self.elements[0]
        return None