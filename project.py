# --------------------- Data Structures Used --------------------- #

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class CustomLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def traverse(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.data)
            current = current.next
        return tasks

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        return data

    def is_empty(self):
        return self.top is None

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, task):
        self.heap.append(task)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index].priority < self.heap[parent_index].priority:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_task = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_task

    def _heapify_down(self, index):
        while index < len(self.heap):
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < len(self.heap) and self.heap[left_child].priority < self.heap[smallest].priority:
                smallest = left_child
            if right_child < len(self.heap) and self.heap[right_child].priority < self.heap[smallest].priority:
                smallest = right_child

            if smallest == index:
                break
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest

    def peek(self):
        return self.heap[0] if self.heap else None
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if not self.front:
            return None
        data = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        return data

    def is_empty(self):
        return self.front is None

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.tasks = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, task):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.tasks.append(task)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.tasks if node.is_end_of_word else []

class TreeNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, task):
        if not self.root:
            self.root = TreeNode(task)
        else:
            self._insert(self.root, task)

    def _insert(self, node, task):
        if task.priority < node.task.priority:
            if not node.left:
                node.left = TreeNode(task)
            else:
                self._insert(node.left, task)
        else:
            if not node.right:
                node.right = TreeNode(task)
            else:
                self._insert(node.right, task)

    def inorder(self, node=None, tasks=None):
        if tasks is None:
            tasks = []
        if node:
            self.inorder(node.left, tasks)
            tasks.append(node.task)
            self.inorder(node.right, tasks)
        return tasks

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_task(self, task):
        if task.task_id not in self.adj_list:
            self.adj_list[task.task_id] = []

    def add_dependency(self, task_id_1, task_id_2):
        if task_id_1 in self.adj_list:
            self.adj_list[task_id_1].append(task_id_2)

    def get_dependencies(self, task_id):
        return self.adj_list.get(task_id, [])

# --------------------- Task Management --------------------- #

class Task:
    task_counter = 1

    def __init__(self, title, description, priority, deadline):
        self.task_id = Task.task_counter
        Task.task_counter += 1
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline

    def __str__(self):
        return f"Task {self.task_id}: {self.title} (Priority: {self.priority}, Deadline: {self.deadline})"

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.tasks = CustomLinkedList()

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        current = self.tasks.head
        while current:
            if current.data.task_id == task_id:
                self.tasks.remove(current.data)
                return True
            current = current.next
        return False

    def list_tasks(self):
        return self.tasks.traverse()

class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}  # Global HashMap for tasks by task_id
        self.scheduler = TaskScheduler()
        self.task_search_trie = Trie()
        self.sorted_task_bst = BST()
        self.task_dependency_graph = Graph()

    def add_user(self, user_id, username):
        self.users[user_id] = User(user_id, username)

    def add_task(self, user_id, title, description, priority, deadline):
        if user_id in self.users:
            task = Task(title, description, priority, deadline)
            self.users[user_id].add_task(task)
            self.tasks[task.task_id] = task  # Add to global task dictionary
            self.task_search_trie.insert(title, task)  # Insert title into Trie for search
            self.sorted_task_bst.insert(task)  # Insert task into BST for sorting
            self.task_dependency_graph.add_task(task)  # Add task to graph
            return task
        else:
            return None

    def remove_task(self, user_id, task_id):
        if user_id in self.users and task_id in self.tasks:
            if self.users[user_id].remove_task(task_id):
                del self.tasks[task_id]
                return True
        return False

    def get_tasks_by_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id].list_tasks()
        return []

    def add_dependency(self, task_id_1, task_id_2):
        # Ensure tasks exist before adding dependency
        if task_id_1 in self.tasks and task_id_2 in self.tasks:
            self.task_dependency_graph.add_dependency(task_id_1, task_id_2)

# --------------------- Undo/Redo Manager --------------------- #

class UndoRedoManager:
    def __init__(self):
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def perform_action(self, action):
        self.undo_stack.push(action)
        self.redo_stack = Stack()  # Clear redo stack

    def undo(self):
        action = self.undo_stack.pop()
        if action:
            # Push the action to redo stack to allow redoing it later
            self.redo_stack.push(action)
        return action

    def redo(self):
        action = self.redo_stack.pop()
        if action:
            # Push the action back to undo stack as it's being redone
            self.undo_stack.push(action)
        return action

# --------------------- Task Scheduler --------------------- #

class TaskScheduler:
    def __init__(self):
        self.heap = MinHeap()

    def schedule_task(self, task):
        self.heap.insert(task)

    def get_next_task(self):
        return self.heap.extract_min()

# --------------------- Console-Based UI --------------------- #

def main():
    task_manager = TaskManager()
    undo_redo = UndoRedoManager()
    scheduler = TaskScheduler()

    while True:
        print("\nTask Management System")
        print("1. Create User")
        print("2. Add Task")
        print("3. List Tasks")
        print("4. Remove Task")
        print("5. Schedule Task")
        print("6. Get Next Task")
        print("7. Undo Last Action")
        print("8. Redo Last Action")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if (choice == '1'):
            user_id = input("Enter User ID: ")
            username = input("Enter Username: ")
            task_manager.add_user(user_id, username)
            print(f"User {username} created.")

        elif choice == '2':
            user_id = input("Enter User ID: ")
            if user_id in task_manager.users:
                title = input("Enter Task Title: ")
                description = input("Enter Task Description: ")
                priority = int(input("Enter Task Priority (lower is higher priority): "))
                deadline = input("Enter Task Deadline: ")
                task = task_manager.add_task(user_id, title, description, priority, deadline)
                if task:
                    undo_redo.perform_action(('add', task))
                    print(f"Task added. Task ID: {task.task_id}")  # Display the task ID here
                else:
                    print("Failed to add task.")
            else:
                print("User Not Found")

        elif (choice == '3'):
            user_id = input("Enter User ID: ")
            tasks = task_manager.get_tasks_by_user(user_id)
            if tasks:
                for task in tasks:
                    print(task)
            else:
                print("No tasks found for this user.")

        elif choice == '4':
            user_id = input("Enter User ID: ")
            task_id = int(input("Enter Task ID to remove: "))
            if task_manager.remove_task(user_id, task_id):
                undo_redo.perform_action(('remove', task_id))
                print("Task removed.")
            else:
                print("Task not found or could not be removed.")

        elif choice == '5':
            user_id = input("Enter User ID: ")
            task_id = int(input("Enter Task ID to schedule: "))
            if task_id in task_manager.tasks:
                scheduler.schedule_task(task_manager.tasks[task_id])
                print("Task scheduled.")
            else:
                print("Task not found.")

        elif choice == '6':
            task = scheduler.get_next_task()
            if task:
                print(f"Next Task: {task}")
            else:
                print("No tasks scheduled.")

        elif choice == '7':
            action = undo_redo.undo()
            if action:
                print(f"Undoing action: {action}")
            else:
                print("No actions to undo.")

        elif choice == '8':
            action = undo_redo.redo()
            if action:
                print(f"Redoing action: {action}")
            else:
                print("No actions to redo.")

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()