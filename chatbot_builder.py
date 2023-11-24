from Node import Node


def read_questions(file_path):
    questions = []
    positive_subsets = []
    negative_subsets = []

    with open(file_path, "r") as file:
        lines = file.readlines()

        current_question = None

        for line in lines:
            # Check if the line is not empty and does not contain "Yes:" or "No:"
            if line.strip() and all(
                keyword not in line.lower() for keyword in ["yes:", "no:"]
            ):
                # If true, add the line to the list of questions
                current_question = line.strip()
                questions.append(current_question)
            elif current_question and line.lower().startswith("yes:"):
                # If the current line starts with "Yes:", add the content after "Yes:" to the 'yes' list
                positive_subsets.append(
                    line[len("yes:") :].strip().replace(" ", "").split(",")
                )
            elif current_question and line.lower().startswith("no:"):
                # If the current line starts with "No:", add the content after "No:" to the 'no' list
                negative_subsets.append(
                    line[len("no:") :].strip().replace(" ", "").split(",")
                )

    return questions, positive_subsets, negative_subsets


def get_num_nodes():
    with open("Chatbot questions/encoded_dependencies.txt", "r") as file:
        sequence = file.read()
    max_value = 0
    for line in sequence.split("\n"):
        if line:
            parts = line.split("->")
            value = int(parts[0])

            max_value = max(max_value, value)

    return max_value


def create_nodes(questions, positive_subsets, negative_subsets):
    nodes = []
    for i in range(get_num_nodes()):
        nodes.append(Node(i + 1))

    with open("Chatbot questions/encoded_dependencies.txt", "r") as file:
        while True:
            line1 = file.readline().strip()
            line2 = file.readline().strip()

            if not line2:  # If line2 is empty, we've reached the end of the file
                break

            # Process your two lines here
            parts1 = line1.split("->")
            parts2 = line2.split("->")

            node_index = int(parts1[0]) - 1
            if parts1[1] != "end":
                positive_node = nodes[int(parts1[1]) - 1]
            else:
                positive_node = None

            if parts2[1] != "end":
                negative_node = nodes[int(parts2[1]) - 1]
            else:
                negative_node = None

            current_node = nodes[node_index]
            current_node.build_node(
                positive_node, negative_node, [questions[node_index]]
            )
            if positive_node is not None and positive_node.id > current_node.id:
                positive_node.set_parent(current_node)
                positive_node.set_subset(positive_subsets[node_index])
            if negative_node is not None and negative_node.id > current_node.id:
                negative_node.set_parent(current_node)
                negative_node.set_subset(negative_subsets[node_index])

    return nodes


# Example usage:
file_path = "Chatbot questions/chatbot_questions.txt"
questions, positive_subsets, negative_subsets = read_questions(file_path)
nodes = create_nodes(questions, positive_subsets, negative_subsets)
nodes[9].print_info()
