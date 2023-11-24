def read_questions(file_path):
    questions = []
    yes_subsets = []
    no_subsets = []

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
                yes_subsets.append(line[len("yes:") :].strip())
            elif current_question and line.lower().startswith("no:"):
                # If the current line starts with "No:", add the content after "No:" to the 'no' list
                no_subsets.append(line[len("no:") :].strip())

    return questions, yes_subsets, no_subsets


# Example usage:
file_path = "Chatbot questions/chatbot_questions.txt"
questions, yes_subsets, no_subsets = read_questions(file_path)

# Print the extracted questions
for i, question in enumerate(questions, start=1):
    print(f"{i}. {question}")

# Print the 'yes' subsets
print("\nYes Subsets:")
for subset in yes_subsets:
    print(subset)

# Print the 'no' subsets
print("\nNo Subsets:")
for subset in no_subsets:
    print(subset)

