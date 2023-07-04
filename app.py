import glob
import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_files = request.files.getlist('json_files')
        output_dir = request.form.get('output_dir', './')
        output_filename = request.form.get(
            'output_filename', 'docker-compose.yml')

        # Save the uploaded JSON files
        json_directory = save_uploaded_files(json_files)

        generate_docker_compose(json_directory, output_dir, output_filename)
        return redirect('/success')

    return render_template('index.html')


def save_uploaded_files(files):
    json_directory = './uploaded_jsons'
    os.makedirs(json_directory, exist_ok=True)

    for file in files:
        file_path = os.path.join(json_directory, file.filename)
        file.save(file_path)

    return json_directory


def get_json_files(directory):
    json_files = glob.glob(os.path.join(directory, '*.json'))
    return json_files


def generate_docker_compose(json_directory, output_dir, output_filename):
    docker_compose = []
    docker_compose.append("version: '3'\n\nservices:\n")
    service_names = []

    json_files = get_json_files(json_directory)

    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                config = json.load(file)

            for service_name, service_config in config.items():
                if service_name in service_names:
                    print(
                        f"Warning: Duplicate service name '{service_name}' in '{json_file}'. Skipping.")
                    continue

                service_names.append(service_name)
                docker_compose.append(f"  {service_name}:\n")
                docker_compose.append("    image: {}\n".format(
                    service_config.get('image', '')))
                docker_compose.append("    ports:\n")
                for port in service_config.get('ports', []):
                    docker_compose.append(f"      - {port}\n")
                docker_compose.append("    command: {}\n".format(
                    service_config.get('command', '')))
                docker_compose.append("\n")
        except FileNotFoundError:
            print(f"Error: JSON file '{json_file}' not found.")
            return
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{json_file}'.")
            return

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(output_path, "w") as file:
            file.writelines(docker_compose)
        print(f"Docker Compose file '{output_path}' generated successfully!")
    except IOError:
        print(
            f"Error: Failed to write Docker Compose file '{output_path}'. Check the output directory.")
        return


@app.route('/success')
def success():
    return "Docker Compose YAML generated successfully!"


if __name__ == '__main__':
    app.debug = True
    app.run()
