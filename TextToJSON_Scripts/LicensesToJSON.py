import os
import json


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    # print(files)
    return files


def license_to_json(folder_path):
    licenses = []
    filenames = list_files_in_directory(folder_path)
    for filename in filenames:
        with open(folder_path + filename, "r") as file:
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
                spdx_id = line[len("spdx-id:") :].strip()
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

        instance_data = {
            "title": title,
            "spdx-id": spdx_id,
            "description": description,
            "permissions": permissions,
            "conditions": conditions,
            "limitations": limitations,
        }
        folder_path2 = "../newJSON"  # Replace with the desired folder path

        # Ensure the specified folder exists
        if not os.path.exists(folder_path2):
            os.makedirs(folder_path2)

        # Construct the full file path
        file_path = os.path.join(folder_path2, spdx_id + ".json")
        # Convert Python dictionary to JSON format
        json_data = json.dumps(instance_data, indent=2)

        # Write JSON data to a file
        with open(file_path, "w") as json_file:
            json_file.write(json_data)


license_to_json("../_licenses/")
