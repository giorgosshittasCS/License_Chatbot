from Node import Node
from Tree import Tree
from License import License
import os
import asyncio
import json
import datetime


from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS  # Import CORS


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    # print(files)
    return files


def read_licenses():
    licenses = []
    filenames = list_files_in_directory("_licenses/")
    for filename in filenames:
        with open("_licenses/" + filename, "r") as file:
            lines = file.readlines()
        permissions = []
        conditions = []
        limitations = []
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("description: "):
                description = line[len("description:") :].strip()
            elif line.startswith("title: "):
                title = line[len("title:") :].strip()
            elif line.startswith("spdx-id: "):
                id = line[len("spdx-id:") :].strip()
            if line.startswith("permissions:"):
                j = i + 1
                line = lines[j].strip()
                while line.startswith("-"):
                    permissions.append(line[1:].strip())
                    j = j + 1
                    line = lines[j].strip()
            if line.startswith("conditions:"):
                j = i + 1
                line = lines[j].strip()
                while line.startswith("-"):
                    conditions.append(line[1:].strip())
                    j = j + 1
                    line = lines[j].strip()
            if line.startswith("limitations:"):
                j = i + 1
                line = lines[j].strip()
                while line.startswith("-"):
                    limitations.append(line[1:].strip())
                    j = j + 1
                    line = lines[j].strip()

        license = License()
        license.set_info(conditions, limitations, permissions, title, description, id)
        licenses.append(license)

    return licenses


def read_licenses2():
    licenses = []
    filenames = list_files_in_directory("Licenses_JSON/")
    for filename in filenames:
        with open("Licenses_JSON/" + filename, "r") as file:
            data = json.load(file)

        title = data["title"]
        spdx_id = data["spdx-id"]
        description = data["description"]
        permissions = data["permissions"]
        conditions = data["conditions"]
        limitations = data["limitations"]

        # Store conditions, limitations, permissions in a list
        values_list = [
            conditions,
            limitations,
            permissions,
            title,
            description,
            spdx_id,
        ]

        # Print the list
        print(values_list)

        license = License()
        license.set_info(
            conditions, limitations, permissions, title, description, spdx_id
        )
        licenses.append(license)

    return licenses
    # print("Description: " + description)
    # print("Permissions: ", permissions)
    # print("Conditions: ", conditions)
    # print("Limitations:", limitations)
    # print("Title: " + title)
    # print("Id: " + id)


def read_questions(filepath, licenses):
    key_questions = {}
    positive_subsets = []
    negative_subsets = []
    with open(filepath, "r") as file:
        data = json.load(file)

    # Extract the arrays from the JSON data
    questions = data["questions"]
    keys = data["keys"]

    for i in range(len(keys)):
        key_questions[keys[i]] = questions[i]

    for key, value in key_questions.items():
        questions.append(value)
        positive_subset = []
        negative_subset = []
        for license in licenses:
            if "None" in key:
                positive_subset.append(license.id)
                negative_subset.append(license.id)
            else:
                if key.startswith("!"):
                    if license.all_rights[key[1:]]:
                        negative_subset.append(license.id)
                    else:
                        positive_subset.append(license.id)
                else:
                    if license.all_rights[key]:
                        positive_subset.append(license.id)
                    else:
                        negative_subset.append(license.id)

        positive_subsets.append(positive_subset)
        negative_subsets.append(negative_subset)

    return questions, positive_subsets, negative_subsets

    # def read_questions2(file_path, licenses):
    #     key_questions = {}
    #     questions = []
    #     positive_subsets = []
    #     negative_subsets = []

    #     with open(file_path, "r") as file:
    #         lines = file.readlines()

    #         current_question = None

    #         for line in lines:
    #             if line.strip():
    #                 parts = line.split("|")
    #                 key_questions[parts[1][len(" key: ") :].strip()] = parts[0].strip()

    #         for key, value in key_questions.items():
    #             questions.append(value)
    #             positive_subset = []
    #             negative_subset = []
    #             for license in licenses:
    #                 if "None" in key:
    #                     positive_subset.append(license.id)
    #                     negative_subset.append(license.id)
    #                 else:
    #                     if key.startswith("!"):
    #                         if license.all_rights[key[1:]]:
    #                             negative_subset.append(license.id)
    #                         else:
    #                             positive_subset.append(license.id)
    #                     else:
    #                         if license.all_rights[key]:
    #                             positive_subset.append(license.id)
    #                         else:
    #                             negative_subset.append(license.id)

    #             positive_subsets.append(positive_subset)
    #             negative_subsets.append(negative_subset)

    # print("\n Positive: \n")
    # for license in positive_subsets[0]:
    #     print(license.title)
    # print("\n Negative: \n")
    # for license in negative_subsets[0]:
    #     print(license.title)

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
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        line_index = 0

    while line_index < len(lines):
        line1 = lines[line_index]
        line2 = lines[line_index + 1]
        line3 = lines[line_index + 2]

        # Process your two lines here
        parts1 = line1.replace(" ", "").split("->")
        parts2 = line2.replace(" ", "").split("->")
        parts3 = line3.replace(" ", "").split("->")

        node_index = int(parts1[0]) - 1

        if parts1[1] != "end":
            positive_node = nodes[int(parts1[1]) - 1]
        else:
            positive_node = None

        if parts2[1] != "end":
            negative_node = nodes[int(parts2[1]) - 1]
        else:
            negative_node = None

        if parts3[1] == "end" or parts3[1] == "none":
            neutral_node = None
        else:
            neutral_node = nodes[int(parts3[1]) - 1]

        current_node = nodes[node_index]
        current_node.build_node(
            positive_node,
            neutral_node,
            negative_node,
            [questions[node_index]],
            positive_subsets[node_index],
            negative_subsets[node_index],
        )
        if positive_node is not None and positive_node.id > current_node.id:
            positive_node.set_parent(current_node)
            # positive_node.set_subset(positive_subsets[node_index])
        if negative_node is not None and negative_node.id > current_node.id:
            negative_node.set_parent(current_node)
            # negative_node.set_subset(negative_subsets[node_index])

        line_index = line_index + 3

    return nodes


# Example usage:
file_path = "Chatbot Questions/JSON_questions.json"
licenses = read_licenses2()
questions, positive_subsets, negative_subsets = read_questions(file_path, licenses)
nodes = create_nodes(questions, positive_subsets, negative_subsets)


tree = Tree(nodes, nodes[0], set(positive_subsets[0]).union(set(negative_subsets[0])))

directory_path = "UI/static/app2/build/static/js"
files = []
for filename in os.listdir(directory_path):
    if os.path.isfile(os.path.join(directory_path, filename)):
        files.append(filename)
filtered_files = [
    file for file in files if file.startswith("main") and file.endswith("js")
]
mainjs = filtered_files[0]

app = Flask(
    __name__,
    template_folder="UI/templates",
    static_folder="UI/static",
)
CORS(app)

x = datetime.datetime.now()


@app.route("/")
def root():
    return "hello"


@app.route("/data")
def get_time():
    # Returning an api for showing in  reactjs
    return {"Name": "geek", "Age": "22", "Date": x, "programming": "python"}


@app.route("/welcome")
def index():
    asyncio.run(tree.start_questionnaire2(None))
    dummy_data = {"hello": "world", "welcome": "to the questionnaire"}
    return json.dumps(dummy_data)


@app.route("/question", methods=["POST"])
def question():
    data = request.json
    answer = data.get("answer")
    result = asyncio.run(
        tree.start_questionnaire2(answer)
    )  # Run the asynchronous function
    return jsonify(result)


@app.route("/chatbot")
def chatbot():
    print("Hello world")
    return render_template("chatbot2.html")


if __name__ == "__main__":
    app.run()
