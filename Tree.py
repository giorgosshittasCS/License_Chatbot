class Tree:
    def __init__(self, nodes, parent, initial_subset):
        self.nodes = nodes
        self.parent = parent
        self.initial_subset = [license for license in list(initial_subset)]
        self.current_node = parent
        self.current_subset = [license for license in list(initial_subset)]

    def positive_answer(self):
        self.current_subset = list(
            set(self.current_subset).intersection(
                set(self.current_node.positive_subset)
            )
        )
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.left_child is None:
            return 0

        # TODO: when i move back there is an issue
        elif self.current_node.left_child.id < self.current_node.id:
            self.current_subset = [
                license for license in self.current_node.left_child.current_subset
            ]
            return 0

        self.current_node = self.current_node.left_child
        return 1

    def negative_answer(self):
        self.current_subset = list(
            set(self.current_subset).intersection(
                set(self.current_node.negative_subset)
            )
        )
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.right_child is None:
            return 0

        elif self.current_node.right_child.id < self.current_node.id:
            self.current_subset = [
                license for license in self.current_node.right_child.current_subset
            ]
            return 0

        self.current_node = self.current_node.right_child
        return 1

    def neutral_answer(self):
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.middle_child is None:
            return 0

        self.current_node = self.current_node.middle_child
        return 1

    def start_questionnaire(self):
        self.current_node = self.parent
        questions = 1
        answer = None
        while questions:
            print(
                "\n ------------------------------------------------------------------------------------------ \n"
            )
            print("     " + self.current_node.questions[0])
            print(
                "\n ------------------------------------------------------------------------------------------ \n"
            )
            answer = input("Answer: ")

            if answer == "yes" or answer == "Yes" or answer == "y":
                questions = self.positive_answer()
            elif answer == "no" or answer == "No" or answer == "n":
                questions = self.negative_answer()
            else:
                questions = self.neutral_answer()

            self.current_node.print_info()
            print("Current Subset: ", self.current_subset)

    async def start_questionnaire2(self, request):
        if request == "yes" or request == "Yes" or request == "y":
            questions = self.positive_answer()
        elif request == "no" or request == "No" or request == "n":
            questions = self.negative_answer()
        elif request == "Don't Mind" or request == "dm":
            questions = self.neutral_answer()

        question = self.current_node.questions[0]
        current_subset = self.current_subset
        options = ["Yes", "No"]
        if self.current_node.middle_child is not None:
            options.append("Don't Mind")
        return {
            "question": question,
            "current_subset": current_subset,
            "options": options,
        }

    def refresh(self):
        self.current_node = self.parent
        self.current_subset = self.initial_subset
