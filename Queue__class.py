class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def put(self, data):
        new_node = Node(data)
        if self.empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def get(self):
        if self.empty():
            raise IndexError("Queue is empty")
        data = self.head.data
        next_node=self.head.next
        del self.head
        self.head = next_node
        self._size -= 1
        if self.empty():  
           self.tail = None  
        return data

    def empty(self):
        return self._size == 0

    def size(self):
        return self._size
    
    def clear(self):
        current = self.head
        while current:
            next_node = current.next
            del current
            current = next_node
        self.head = None
        self.tail = None
        self._size = 0
   
    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result    

