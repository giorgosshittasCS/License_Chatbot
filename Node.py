class Node:
    def __init__(self, id):
        self.questions = None
        self.left_child = None
        self.right_child = None
        self.id = id
        self.subset = None

    def build_node(self, left_child, right_child, questions):
        self.set_questions(questions)
        self.set_left_child(left_child)
        self.set_right_child(right_child)

    def set_subset(self, subset):
        self.subset = [license for license in subset]

    def set_left_child(self, left_node):
        self.left_child = left_node

    def set_right_child(self, right_node):
        self.right_child = right_node

    def set_parent(self, parent):
        self.parent = parent

    def set_questions(self, questions):
        self.questions = [question for question in questions]

    def print_info(self):
        if self.parent is not None:
            print("Parent:", self.parent.id)
        print("Questions:", self.questions)
        if self.right_child is not None:
            print("Right child:", self.right_child.id)
        if self.left_child is not None:
            print("Left child:", self.left_child.id)
        print("Subset:", self.subset)
