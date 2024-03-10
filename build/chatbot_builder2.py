from Node import Node
from Tree import Tree
from License import License
import os
import asyncio
import json
from flask import Flask, render_template, jsonify, request


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


def read_file_paths():
    config_file_path = "../file paths/filepaths.json"

    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)

    return {
        "questions_file": config_data["questions_file"],
        "licenses_folder": config_data["licenses_folder"],
        "dependencies_file": config_data["dependencies_file"],
        "templates_folder": config_data["templates_folder"],
        "static_folder": config_data["static_folder"],
    }


def read_licenses2(folder_path):
    licenses = []
    filenames = list_files_in_directory(folder_path)
    for filename in filenames:
        with open(folder_path + filename, "r") as file:
            data = json.load(file)

        title = data["title"]
        spdx_id = data["spdx-id"]
        description = data["description"]
        permissions = data["permissions"]
        conditions = data["conditions"]
        limitations = data["limitations"]

        license = License()
        license.set_info(
            conditions, limitations, permissions, title, description, spdx_id
        )
        licenses.append(license)

    return licenses


def read_questions(filepath, licenses):
    key_questions = {}
    positive_subsets = []
    negative_subsets = []
    with open(filepath, "r") as file:
        data = json.load(file)

    # Extract the arrays from the JSON data
    questions = data["questions"]
    keys = data["keys"]
    question_explanations = data["question_explanations"]

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

    return questions, positive_subsets, negative_subsets, question_explanations


def get_num_nodes(file_path):
    with open(file_path, "r") as file:
        sequence = file.read()
    max_value = 0
    for line in sequence.split("\n"):
        if line:
            parts = line.split("->")
            value = int(parts[0])

            max_value = max(max_value, value)

    return max_value


def create_nodes(
    file_path, questions, positive_subsets, negative_subsets, question_explanations
):
    nodes = []
    for i in range(get_num_nodes(file_path)):
        nodes.append(Node(i + 1))

    with open(file_path, "r") as file:
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
        options = ["Yes", "No"]

        if parts1[1] != "end":
            positive_node = nodes[int(parts1[1]) - 1]
        else:
            positive_node = None

        if parts2[1] != "end":
            negative_node = nodes[int(parts2[1]) - 1]
        else:
            negative_node = None

        if parts3[1] == "end":
            neutral_node = None
            options.append("Don't Care")
        elif parts3[1] == "none" or parts3[1] == "None":
            neutral_node = None
        else:
            neutral_node = nodes[int(parts3[1]) - 1]
            options.append("Don't Care")

        current_node = nodes[node_index]
        current_node.build_node(
            positive_node,
            neutral_node,
            negative_node,
            [questions[node_index]],
            positive_subsets[node_index],
            negative_subsets[node_index],
            options,
            question_explanations[node_index],
        )
        if positive_node is not None and positive_node.id > current_node.id:
            positive_node.set_parent(current_node)
            # positive_node.set_subset(positive_subsets[node_index])
        if negative_node is not None and negative_node.id > current_node.id:
            negative_node.set_parent(current_node)
            # negative_node.set_subset(negative_subsets[node_index])

        line_index = line_index + 3

    return nodes


async def getLicenseInfo(all_licenses, license_ids):
    licenses = []
    licenses_titles = []
    print(all_licenses)
    print("----------------------------------------------------------------")
    print(license_ids)
    for id in license_ids:
        for license in all_licenses:
            if id == license.id:
                licenses.append(
                    [license.permissions, license.conditions, license.limitations]
                )
                licenses_titles.append(license.title)

    return {
        "licenses": licenses,
        "licenses_titles": licenses_titles,
    }


# Example usage:
paths = read_file_paths()
licenses = read_licenses2(paths.get("licenses_folder"))
questions, positive_subsets, negative_subsets, question_explanations = read_questions(
    paths.get("questions_file"), licenses
)
nodes = create_nodes(
    paths.get("dependencies_file"),
    questions,
    positive_subsets,
    negative_subsets,
    question_explanations,
)

tree = Tree(nodes, nodes[0], set(positive_subsets[0]).union(set(negative_subsets[0])))

app = Flask(
    __name__,
    template_folder=paths.get("templates_folder"),
    static_folder=paths.get("static_folder"),
)


@app.route("/")
def index():
    asyncio.run(tree.start_questionnaire2(None))  # Run the asynchronous function
    return render_template("index.html")


@app.route("/question", methods=["POST"])
def question():
    data = request.json
    answer = data.get("answer")
    result = asyncio.run(
        tree.start_questionnaire2(answer)
    )  # Run the asynchronous function
    return jsonify(result)


@app.route("/table", methods=["POST"])
def fetch_info():
    result = asyncio.run(getLicenseInfo(licenses, tree.current_subset))
    return jsonify(result)


@app.route("/chatbot")
def chatbot():
    tree.refresh()
    return render_template(
        "chatbot.html",
        question=tree.current_node.questions[0],
        current_subset=tree.initial_subset,
        question_explanation=tree.current_node.question_explanation,
    )


if __name__ == "__main__":
    app.run()
